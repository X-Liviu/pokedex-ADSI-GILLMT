import json

from app.controller.model.equipo_controller import Equipo


class Usuario:
    def __init__(self, nombre: str, apellido: str, nombre_usuario: str, correo: str, contrasena: str, rol: str, lista_equipos: list):
        self.nombre = nombre
        self.apellido = apellido
        self.nombre_usuario = nombre_usuario
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol
        self.lista_equipos = lista_equipos
        # self.amigos = []

    def addEquipo(self) :
        if self.tieneEquipos() :
            ultimo_num = max(equipo.numEquipo for equipo in self.lista_equipos)
            numEquipo = ultimo_num + 1
        else:
            numEquipo = 1

        nuevo_equipo = Equipo(numEquipo)
        self.lista_equipos.append(nuevo_equipo)
        return nuevo_equipo.numEquipo

    def buscarEquipo(self, numEquipo: int):
        for equipo in self.lista_equipos:
            if equipo.esEsteEquipo(numEquipo):
                return equipo
        return None

    def tieneEquipos(self):
        if self.lista_equipos:
            return True
        else:
            return False

    def obtenerEquipos(self):
        numeros_id = []
        for equipo in self.lista_equipos:
            numeros_id.append(equipo.id)

        return numeros_id

    def exportarEquiposJSON(self):
        # Obtenemos la lista de números
        lista_nums = self.obtenerEquipos()

        # Creamos un diccionario para darle estructura al JSON
        datos = {
            "usuario": self.nombreUsuario,
            "cantidad": len(lista_nums),
            "ids_equipos": lista_nums
        }

        # Convertimos el diccionario a una cadena de texto formato JSON
        return json.dumps(datos, indent=4)

    def mejorPokemon(self, numEquipo):
        elEquipo = self.buscarEquipo(numEquipo)
        if elEquipo != None :
            return elEquipo.getMejorPokemon()
        else:
            return -1

    def ainadirAmigo(self, nombre):
        resultado = False
        if not self._esAmigo(nombre):
            pass
            # nuevoAmigo = Usuario()
            # self.lista_amigos.append(nuevoAmigo)
        return resultado

    """
    def _esAmigo(self, nombre):
        resultado = False
        indice = 0
        longitud = len(self.amigos)
        while not resultado and indice < longitud:
            if self.amigos[indice].esNombre(nombre):
                resultado = not resultado
            else:
                indice += 1
        return resultado
    """