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

    """
    def mostrarUsuario(self, pNombreUsuario: str, pNombreAmigo: str) -> Custom_types.MarcoDex.Usuario:
        resultado_ranking: Custom_types.Ranking.Usuario = Ranking.getMyRanking(self.db).mostrarUsuario(pNombreAmigo)
        resultado_gestor_usuario: Custom_types.GestorUsuario.EstadoAmigo = gestorUsuario.getMyGestorUsuario(pNombreUsuario, self.db).esMiAmigo(pNombreAmigo)
    
        return {
            "nombre": resultado_ranking["nombre"],
            "equipoEspecie": resultado_ranking["equipoEspecie"],
            "equipoCustom": resultado_ranking["equipoCustom"],
            "fotoPokemon": resultado_ranking["fotoPokemon"],
            "puesto": resultado_ranking["puesto"],
            "estado_amigo": resultado_gestor_usuario["estado_amigo"],
        }
    """

    def mostrarUsuario(self, pNombreUsuario: str, pNombreAmigo: str) -> Custom_types.MarcoDex.Usuario:
        resultado_ranking: Custom_types.Ranking.Usuario = Ranking.getMyRanking(self.db).mostrarUsuario(pNombreAmigo)
        # resultado_gestor_usuario: Custom_types.GestorUsuario.EstadoAmigo = gestorUsuario.getMyGestorUsuario(pNombreUsuario, self.db).esMiAmigo(pNombreAmigo)

        return {
            "nombre": resultado_ranking["nombre"],
            "equipoEspecie": resultado_ranking["equipoEspecie"],
            "equipoCustom": resultado_ranking["equipoCustom"],
            "fotoPokemon": resultado_ranking["fotoPokemon"],
            "puesto": resultado_ranking["puesto"],
            # "estado_amigo": resultado_gestor_usuario["estado_amigo"],
        }

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

    def iniciarSesion(self, pNomUsuario: str, pContrasena: str) -> bool:
        return gestorUsuario.iniciarSesion(pNomUsuario, pContrasena, self.db)

    def getRol(self, nombre_usuario: str) -> str:
        """
        Recupera el rol del usuario (ADMIN, VERIF, NOVERIF)
        para poder decidir a qué pantalla redirigir.
        """
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        # Verificamos que el gestor y el usuario existan para evitar errores
        if gestor and gestor.usuario:
            return gestor.usuario.rol
        return "NOVERIF"

    def procesarRegistro(self, pNom: str, pAp: str, pCorreo: str, pNomUsuario: str, pContrasena: str, pContrasenaRep: str) -> int:
        """
        Coordina el registro de un nuevo usuario.
        Retornos:
           -1: Contraseñas no coinciden
           -2: Usuario o correo duplicado
            0: Éxito
        """
        # Llamamos al método estático del gestor
        return gestorUsuario.registrarUsuario(pNom, pAp, pCorreo, pNomUsuario, pContrasena, pContrasenaRep, self.db)

    def procesarSolicitudModificar(self, pNomUsuario: str, pNom: str, pAp: str, pCorreo: str, pUsuarioNuevo: str, pNuevaContra: str) -> int:
        """
        Retorna:
         0: Modificación directa exitosa
         1: Requiere confirmación con contraseña
        -1: ERROR CRÍTICO (Usuario no encontrado)
        """
        gestor = gestorUsuario.getMyGestorUsuario(pNomUsuario, self.db)

        if gestor is None:
            # El usuario de la sesión no existe en la BD.
            return -1

        # 1. Verificar Cambios
        es_sensible = gestor.verificarCambios(pNomUsuario, pUsuarioNuevo, pNuevaContra)

        if es_sensible:
            gestor.guardarModificacionTemporal(pNomUsuario, pNom, pAp, pCorreo, pUsuarioNuevo, pNuevaContra)
            return 1
        else:
            gestor.modificarUsuarioEnMemoriaYBD(pNom, pAp, pCorreo, pUsuarioNuevo, pNuevaContra)
            return 0

    def confirmarConContraseña(self, pNomUsuario: str, pContraseña: str): #TODO ahora se devuelve el objeto entero, intentar cambiar por String o boolean como lo tenía antes si es posible
        gestor = gestorUsuario.getMyGestorUsuario(pNomUsuario, self.db)
        return gestor.validarCredencialesYGuardarCambios(pNomUsuario, pContraseña)

    # --- MÉTODOS AUXILIARES ---
    def getUsuarioObjeto(self, nombre_usuario):
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        return gestor.usuario if gestor else None

    def pedirUsuariosParaAdmin(self):
        """
        Paso 3 del flujo Aprobar/Borrar/Modificar
        """
        return gestorUsuario.obtenerUsuariosParaAdmin(self.db)

    def procesarAprobadoUsuario(self, pNomUsuario: str) -> bool:
        """
        Paso 13 del flujo Aprobar
        """
        return gestorUsuario.aprobarUsuario(pNomUsuario, self.db)

    def procesarBorradoUsuario(self, pNomUsuario: str):
        """
        Paso 13 del flujo Borrar. Retorna JSON/Lista actualizada.
        """
        return gestorUsuario.borrarUsuario(pNomUsuario, self.db)

    def procesarModificarDatosAdmin(self, pNomUsuario, pNombre, pAp, pNomUsuarioModif) -> bool:
        """
        Paso 15 del flujo Modificar
        """
        try:
            gestorUsuario.modificarUsuarioEnMemoriaPorAdmin(pNomUsuario, pNombre, pAp, pNomUsuarioModif, self.db)
            return True
        except Exception as e:
            print(f"Error procesarModificar: {e}")
            return False

if __name__ == "__main__":
    pass