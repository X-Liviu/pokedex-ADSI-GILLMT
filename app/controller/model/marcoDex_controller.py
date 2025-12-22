import json
import ranking_controller
from app.controller.model.equipo_controller import Equipo
from app.controller.model.gestorUsuario_controller import gestorUsuario


class MarcoDex:
    def __init__(self):
        pass

    def mostrarUsuarios(self) -> str:
        resultado: str = None
        if ranking_controller.Ranking.getMyRankings() != None:
            resultado = ranking_controller.Ranking.getMyRanking().mostrarUsuarios()

        return resultado

    def mostrarUsuario(self, pNombreUsuario: str) -> str:
        resultado: str = None
        if ranking_controller.Ranking.getMyRankings() != None:
            resultado = ranking_controller.Ranking.getMyRanking().mostrarUsuario(pNombreUsuario)

        return resultado

    def newEquipo(self):
        if gestorUsuario.noEsNull() :
            return gestorUsuario.crearEquipo()

    def tieneEquipos(self) :
        return gestorUsuario.tieneEquipos()

    def getListaEquipos(self) :
        return gestorUsuario.getListaEquipos()