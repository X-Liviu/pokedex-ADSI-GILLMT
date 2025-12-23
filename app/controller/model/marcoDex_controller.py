from app.controller.model.ranking_controller import Ranking
from app.custom_types import Custom_types
from app.controller.model.equipo_controller import Equipo
from app.controller.model.gestorUsuario_controller import gestorUsuario

from typing import Dict

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

    def aniadirAmigo(self, nombreUsuario: str) -> Dict[str, bool]:
        resultado: Dict[str, bool] = {"Aniadido": False}
        if gestorUsuario.getMyGestorUsuario() != None:
            resultado["Aniadido"] = gestorUsuario.getMyGestorUsuario().aniadirAmigo(nombreUsuario)

        return resultado

    """
    Las llamadas que se estan haciendo a GestorUsuario no pertenecen a una instancia.
    En ningun momento hemos creado un objeto en ninguna de los metodos. Tampoco se pasa
    una referencia a un objeto por parametros de dichos metodos. Hay que crear una MAE o
    pasar referencia a un objeto creado al inicio de todo por parametros en todos los metodos
    que requiera llamadas a este. Janire en su proyecto de ejemplo crea objetos en la
    constructora de otros(book_controller en loan_controller) 
    """

    def newEquipo(self):
        if gestorUsuario.noEsNull() :
            return gestorUsuario.crearEquipo()

    def tieneEquipos(self) :
        return gestorUsuario.tieneEquipos()

    def getListaEquipos(self) :
        return gestorUsuario.getListaEquipos()