from app.controller.model.ranking_controller import Ranking
from app.custom_types import Custom_types
from app.controller.model.equipo_controller import Equipo
from app.controller.model.gestorUsuario_controller import gestorUsuario


class MarcoDex:
    def __init__(self):
        pass

    def mostrarUsuarios(self) -> Custom_types.Ranking.Usuarios:
        resultado: Custom_types.Ranking.Usuarios = {"usuarios": []}
        if Ranking.getMyRankings() != None:
            resultado = Ranking.getMyRanking().mostrarUsuarios()

        return resultado

    def mostrarUsuario(self, pNombreUsuario: str) -> Custom_types.Ranking.Usuario:
        resultado: Custom_types.Ranking.Usuario = {"nombre": pNombreUsuario, "equipoEspecie": [], "equipoCustom": []}
        if Ranking.getMyRankings() != None:
            resultado = Ranking.getMyRanking().mostrarUsuario(pNombreUsuario)

        return resultado

    def aniadirAmigo(self, nombreUsuario1: str, nombreUsuario2: str) -> Custom_types.Ranking.AmigoAniadido:
        resultado: Custom_types.Ranking.AmigoAniadido = {"Aniadido": False}
        if Ranking.getMyRanking() != None:
            resultado = Ranking.getMyRanking().aniadirAmigo(nombreUsuario1, nombreUsuario2)

        return resultado

    def newEquipo(self):
        if gestorUsuario.noEsNull() :
            return gestorUsuario.crearEquipo()

    def tieneEquipos(self) :
        return gestorUsuario.tieneEquipos()

    def getListaEquipos(self) :
        return gestorUsuario.getListaEquipos()