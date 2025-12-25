import sqlite3

class gestorUsuario:
    def __init__(self, db, usuario) :
        self.db = db
        self.usuario = usuario
        pass

    def noEsNull(self):
        return self.usuario is None

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