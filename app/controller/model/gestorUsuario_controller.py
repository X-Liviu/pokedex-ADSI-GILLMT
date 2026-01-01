import sqlite3
from app.controller.model.gestorCopiasEquipo_controller import gestorCopiasEquipo
from app.model.usuario import Usuario

class gestorUsuario:
    _instancias_usuarios = {}
    def __init__(self, db, usuario) :
        self.db = db
        self.usuario = usuario
        pass

    @classmethod
    def getMyGestorUsuario(cls, nombre_usuario, db):
        if nombre_usuario not in cls._instancias_usuarios:
            # 1. Creamos el objeto Usuario completo primero
            usuario = db.getUsuario(nombre_usuario)

            # 2. Creamos el gestor pasándole el objeto completo
            cls._instancias_usuarios[nombre_usuario] = cls(db, usuario)

        return cls._instancias_usuarios[nombre_usuario]

    def crearEquipo(self) :
        return self.usuario.addEquipo()

    def aniadirPokemon(self, nombreEspecie, nombrePokemon, numEquipo):
        equipo = self.usuario.buscarEquipo(numEquipo)
        if not equipo.tiene6():
            return equipo.addPokemon(nombreEspecie, nombrePokemon)
        else:
            return -1

    def guardarEquipo(self, numEquipo):
        self.usuario.guardarEquipo(numEquipo)

    def tieneEquipos(self) :
        return self.usuario.tieneEquipos()

    def getListaEquipos(self) :
        return self.usuario.exportarEquiposJSON()

    def mostrarInfoEquipo(self, numEquipo) :
        equipo = self.usuario.buscarEquipo(numEquipo)
        return equipo.mostrarInfoEquipo()

    def clonarEquipo(self, numEquipo) :
        gestorCopiasEquipo.clonarEquipo(self.usuario, numEquipo)

    def borrarPokemon(self, numEquipo, idPokemon):
        equipo = self.usuario.buscarEquipo(numEquipo)
        if equipo:
            equipo.borrarPokemon(idPokemon)

    def compararCopias(self,numEquipo) :
        gestorCopiasEquipo.compararCopiasEliminar(self.usuario, numEquipo)
        gestorCopiasEquipo.compararCopiasAniadir(self.usuario, numEquipo)
        gestorCopiasEquipo.finalizarEdicion(self.usuario.nombre_usuario)

    def descartarCambios(self, numEquipo) :
        gestorCopiasEquipo.descartarCambios(self.usuario, numEquipo)

    def mejorPokemon(self, numEquipo) :
        return self.usuario.mejorPokemon(numEquipo)

    # Marco lo usa en el Ranking, pero pertence a esta clase
    def aniadirAmigo(self, nombreUsuario: str) -> bool:
        """
        pre: Se da por hecho que "nombreUsuario" no esta vacio
        post: Ainade al usuario que se encuentra como atributo y
        el que esta como parametro en sus listas de amigos. Si
        salio bien, devuelve True y en caso contrario False.
        """
        resultado: bool = self.usuario.ainadirAmigo(nombreUsuario)

        if resultado:
            comandosSQL: str = f"""
             INSERT INTO Amigo_de (NombreUsuario1, NombreUsuario2)
             VALUES ( {self.usuario.getName()}, {nombreUsuario} );
            """

            try:
                self.db.insert(comandosSQL)
            except sqlite3.Error:
                resultado = not resultado

        return resultado