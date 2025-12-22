import json
import ranking_controller
from app.controller.model.gestorUsuario_controller import gestorUsuario


class MarcoDex:
    def __init__(self):
        pass

    def mostrarUsuarios(self) -> str:
        return ranking_controller.mostrarUsuarios()

    def tieneEquipos(self) :
        return gestorUsuario.tieneEquipos()

    def getListaEquipos(self) :
        return gestorUsuario.getListaEquipos()