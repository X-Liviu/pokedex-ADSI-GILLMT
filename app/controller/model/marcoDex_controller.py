import string

from app.controller.model.chatbot_controller import ChatBot
from app.controller.model.gestorPokeDex_controller import gestorPokeDex
from app.controller.model.pokeDex_controller import PokeDex
from app.controller.model.ranking_controller import Ranking
from app.model.utils.custom_types import Custom_types
from app.database.connection import Connection
from app.controller.model.gestorUsuario_controller import gestorUsuario
from app.controller.model.gestorNoticias_controller import gestorNoticias

from typing import Dict

class MarcoDex: pass # Es necesario sino, la linea 12 (myMarcoDex: MarcoDex = None) no funciona

class MarcoDex:
    myMarcoDex: MarcoDex = None

    def __init__(self, db: Connection):
        if MarcoDex.myMarcoDex == None:
            self.db: Connection = db
            MarcoDex.myMarcoDex = self
        else:
            raise Custom_types.SingletonError()

    @classmethod  # Igual que los metodos estaticos de Java
    def getMyMarcoDex(cls, db: Connection) -> MarcoDex:
        if cls.myMarcoDex == None:
            MarcoDex(db)
        return cls.myMarcoDex

    def mostrarRanking(self) -> Custom_types.Ranking.Usuarios:
        return Ranking.getMyRanking(self.db).mostrarRanking()

    def mostrarUsuario(self, pNombreUsuario: str) -> Custom_types.Ranking.Usuario:
        return Ranking.getMyRanking(self.db).mostrarUsuario(pNombreUsuario)

    def aniadirAmigo(self, nombreUsuario: str) -> Dict[str, bool]:
        resultado: Dict[str, bool] = {"Aniadido": False}
        resultado["Aniadido"] = gestorUsuario.getMyGestorUsuario(self.db).aniadirAmigo(nombreUsuario)

        return resultado

    """
    --PARA TABATA-- Las llamadas que se estan haciendo a GestorUsuario no pertenecen a una instancia
    u objeto. En ningun momento hemos creado un objeto en ninguna de los metodos. Tampoco se pasa
    una referencia a un objeto por parametros de dichos metodos. Hay que crear una MAE o
    pasar referencia a un objeto creado al inicio de todo por parametros en todos los metodos
    que requiera llamadas a este. Janire en su proyecto de ejemplo crea objetos en la
    constructora de otros(book_controller en loan_controller) 
    """

    def newEquipo(self, nombre_usuario: str):
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        return gestor.crearEquipo()

    def aniadirPokemon(self, nombreEspecie: str, nombrePokemon: str, numEquipo: int, nombre_usuario: str):
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        return gestor.aniadirPokemon(nombreEspecie, nombrePokemon, numEquipo)

    def guardarEquipo(self, numEquipo: int, nombre_usuario: str):
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        gestor.guardarEquipo(numEquipo)

    def tieneEquipos(self, nombre_usuario: str) :
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        return gestor.tieneEquipos()

    def getListaEquipos(self, nombre_usuario: str) :
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        return gestor.getListaEquipos()

    def clonarEquipo(self, numEquipo: int, nombre_usuario: str):
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        gestor.clonarEquipo(numEquipo)

    def mostrarInfoEquipo(self, numEquipo: int, nombre_usuario: str):
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        return gestor.mostrarInfoEquipo(numEquipo)

    def borrarPokemon(self, numEquipo: int, idPokemon: int, nombre_usuario: str):
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        gestor.borrarPokemon(numEquipo, idPokemon)

    def compararCopias(self,numEquipo: int, nombre_usuario: str):
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        gestor.compararCopias(numEquipo)

    def borrarEquipo(self, numEquipo: int, nombre_usuario: str):
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        return gestor.borrarEquipo(numEquipo)

    def descartarCambios(self, numEquipo: int, nombre_usuario: str):
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        gestor.descartarCambios(numEquipo)

    def mostrarOpciones(self):
        return ChatBot.mostrarOpciones()

    def mejorPokemon(self, numEquipo):
        return gestorUsuario.mejorPokemon(numEquipo)

    def obtenerEfectos(self, nombreEspecie) :
        return gestorPokeDex.obtenerEfectos(nombreEspecie)

    def caracteristicasPokemon(self, nombreEspecie) :
        return gestorPokeDex.caracteristicasPokemon(nombreEspecie)

    def cadenaEvolutiva(self, nombreEspecie) :
        return gestorPokeDex.cadenaEvolutiva(nombreEspecie)

    def tiene_amigos(self, usuario):
        if gestorUsuario.getMyGestorUsuario() != None:
            return gestorUsuario.getMyGestorUsuario().tiene_amigos(usuario)
        return False

    def mostrar_changelog(self, usuario, filtro):
        #clase de gestor_noticia por crear
        return gestorNoticias.getGestorNoticias.mostrar_changelog(usuario,filtro)

    def mostrarPokedex(self) -> str:
        return PokeDex.get_instance().mostrarPokedex()

    def mostrarInfo(self, nombreEspecie: str) -> str:
        return PokeDex.get_instance().getInfo(nombreEspecie)

    def aplicarFiltro(self, filtro: str, valor: str) -> str:
        return PokeDex.get_instance().filtrarPokedex(filtro, valor)

    def tieneAmigos(self) -> bool:
        return gestorUsuario.getMyGestorUsuario().tiene_amigos()

if __name__ == "__main__":
    pass