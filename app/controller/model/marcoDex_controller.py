from app.controller.model.gestorPokeDex_controller import gestorPokeDex
from app.controller.model.ranking_controller import Ranking
from app.model.utils.custom_types import Custom_types
from app.database.connection import Connection
from app.controller.model.gestorUsuario_controller import gestorUsuario
from typing import Dict

class MarcoDex: pass # Es necesario sino, la linea 12 (myMarcoDex: MarcoDex = None) no funciona

class MarcoDex:
    myMarcoDex: MarcoDex = None

    def __init__(self, bd: Connection):
        if MarcoDex.myMarcoDex == None:
            self.bd: Connection = bd
            MarcoDex.myMarcoDex = self
        else:
            raise Custom_types.SingletonError()

    @classmethod # Igual que los metodos estaticos de Java
    def getMyMarcoDex(cls, db: Connection) -> MarcoDex:
        if cls.myMarcoDex == None:
            MarcoDex(db)
        return cls.myMarcoDex

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
    --PARA TABATA-- Las llamadas que se estan haciendo a GestorUsuario no pertenecen a una instancia
    u objeto. En ningun momento hemos creado un objeto en ninguna de los metodos. Tampoco se pasa
    una referencia a un objeto por parametros de dichos metodos. Hay que crear una MAE o
    pasar referencia a un objeto creado al inicio de todo por parametros en todos los metodos
    que requiera llamadas a este. Janire en su proyecto de ejemplo crea objetos en la
    constructora de otros(book_controller en loan_controller) 
    """

    def newEquipo(self):
        if gestorUsuario.getMyGestorUsuario() != None:
            return gestorUsuario.getMyGestorUsuario().crearEquipo()

    def aniadirPokemon(self, nombreEspecie: str, nombrePokemon: str, numEquipo: int):
        if gestorUsuario.getMyGestorUsuario() != None:
            return gestorUsuario.getMyGestorUsuario().aniadirPokemon(nombreEspecie, nombrePokemon, numEquipo)

    def guardarEquipo(self, numEquipo: int):
        if gestorUsuario.getMyGestorUsuario() != None:
            gestorUsuario.getMyGestorUsuario().guardarEquipo(numEquipo)

    def tieneEquipos(self) :
        if gestorUsuario.getMyGestorUsuario() != None:
            return gestorUsuario.getMyGestorUsuario().tieneEquipos()

    def getListaEquipos(self) :
        if gestorUsuario.getMyGestorUsuario() != None:
            return gestorUsuario.getMyGestorUsuario().getListaEquipos()

    def clonarEquipo(self, numEquipo):
        if gestorUsuario.getMyGestorUsuario() != None:
            gestorUsuario.getMyGestorUsuario().clonarEquipo(numEquipo)

    def mostrarInfoEquipo(self, numEquipo):
        if gestorUsuario.getMyGestorUsuario() != None:
            return gestorUsuario.getMyGestorUsuario().mostrarInfoEquipo(numEquipo)

    def borrarPokemon(self, numEquipo, idPokemon):
        if gestorUsuario.getMyGestorUsuario() != None:
            gestorUsuario.getMyGestorUsuario().borrarPokemon(numEquipo, idPokemon)

    def compararCopias(self,numEquipo):
        if gestorUsuario.getMyGestorUsuario() != None:
            gestorUsuario.getMyGestorUsuario().compararCopias(numEquipo)

    def obtenerEfectos(self, nombreEspecie) :
        return gestorPokeDex.obtenerEfectos(nombreEspecie)

    def caracteristicasPokemon(self, nombreEspecie) :
        return gestorPokeDex.caracteristicasPokemon(nombreEspecie)

    def cadenaEvolutiva(self, nombreEspecie) :
        return gestorPokeDex.cadenaEvolutiva(nombreEspecie)

if __name__ == "__main__":
    pass