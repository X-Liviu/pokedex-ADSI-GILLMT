from app.controller.model.gestorPokeDex_controller import gestorPokeDex
from app.controller.model.ranking_controller import Ranking
from app.model.utils.custom_types import Custom_types
from app.database.connection import Connection
from app.controller.model.gestorUsuario_controller import gestorUsuario
from typing import Dict

class MarcoDex: pass # Es necesario sino, la linea 12 (myMarcoDex: MarcoDex = None) no funciona

class MarcoDex:
    myMarcoDex: MarcoDex = None
    usuarios_conectados = {}

    def __init__(self, bd: Connection):
        if MarcoDex.myMarcoDex == None:
            self.bd: Connection = bd
            MarcoDex.myMarcoDex = self
        else:
            raise Custom_types.SingletonError()

    @classmethod  # Igual que los metodos estaticos de Java
    def getMyMarcoDex(cls, db: Connection) -> MarcoDex:
        if cls.myMarcoDex == None:
            MarcoDex(db)

        return cls.myMarcoDex

    @classmethod
    def get_gestor_usuario(cls, nombre_usuario):
        """
        Busca el gestor específico de la persona que está navegando.
        """
        if nombre_usuario not in cls.usuarios_conectados:
            # Si es la primera vez que entra, creamos SU gestor personal
            cls.usuarios_conectados[nombre_usuario] = gestorUsuario(nombre_usuario)

        return cls.usuarios_conectados[nombre_usuario]

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

    def newEquipo(self, nombre_usuario: str):
        gestor = self.get_gestor_usuario(nombre_usuario)
        return gestor.crearEquipo()

    def aniadirPokemon(self, nombreEspecie: str, nombrePokemon: str, numEquipo: int, nombre_usuario: str):
        gestor = self.get_gestor_usuario(nombre_usuario)
        return gestor.aniadirPokemon(nombreEspecie, nombrePokemon, numEquipo)

    def guardarEquipo(self, numEquipo: int, nombre_usuario: str):
        gestor = self.get_gestor_usuario(nombre_usuario)
        gestor.guardarEquipo(numEquipo)

    def tieneEquipos(self, nombre_usuario: str) :
        gestor = self.get_gestor_usuario(nombre_usuario)
        return gestor.tieneEquipos()

    def getListaEquipos(self, nombre_usuario: str) :
        gestor = self.get_gestor_usuario(nombre_usuario)
        return gestor.getListaEquipos()

    def clonarEquipo(self, numEquipo, nombre_usuario):
        gestor = self.get_gestor_usuario(nombre_usuario)
        gestor.clonarEquipo(numEquipo)

    def mostrarInfoEquipo(self, numEquipo, nombre_usuario):
        gestor = self.get_gestor_usuario(nombre_usuario)
        return gestor.mostrarInfoEquipo(numEquipo)

    def borrarPokemon(self, numEquipo, idPokemon, nombre_usuario):
        gestor = self.get_gestor_usuario(nombre_usuario)
        gestor.borrarPokemon(numEquipo, idPokemon)

    def compararCopias(self,numEquipo, nombre_usuario):
        gestor = self.get_gestor_usuario(nombre_usuario)
        gestor.compararCopias(numEquipo)

    def descartarCambios(self, numEquipo,nombre_usuario):
        gestor = self.get_gestor_usuario(nombre_usuario)
        gestor.descartarCambios(numEquipo)

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

    def mostrar_changelog(self, usuario):
        #clase de gestor_noticia por crear
        return self.gestor_noticias.getGestorNoticias.mostrar_changelog(usuario)

    def getNombreUsuario(self):
        #TODO
        return

if __name__ == "__main__":
    pass