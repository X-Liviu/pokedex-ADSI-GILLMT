import json
import ranking_controller
from app.controller.model.equipo_controller import Equipo
from app.controller.model.gestorUsuario_controller import gestorUsuario


class MarcoDex:
    def __init__(self):
        pass

    def mostrarUsuarios(self) -> str:
        return ranking_controller.mostrarUsuarios()

    def newEquipo(self):
        if gestorUsuario.noEsNull() :
            return gestorUsuario.crearEquipo()

    def tieneEquipos(self) :
        return gestorUsuario.tieneEquipos()

    def getListaEquipos(self) :
        return gestorUsuario.getListaEquipos()