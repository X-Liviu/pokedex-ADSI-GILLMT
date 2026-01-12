import string

from app.controller.model.chatbot_controller import ChatBot
from app.controller.model.gestorPokeDex_controller import gestorPokeDex
from app.controller.model.pokeDex_controller import PokeDex
from app.controller.model.ranking_controller import Ranking
from app.model.utils.custom_types import Custom_types
from app.database.connection import Connection
from app.controller.model.gestorUsuario_controller import gestorUsuario
from app.controller.model.gestorNoticias_controller import gestorNoticias
from app.controller.model.gestorAPI_controller import GestorAPI

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
        return ChatBot.getChatBot(self.db).mostrarOpciones()

    def mejorPokemon(self, numEquipo):
        return gestorUsuario.getMyGestorUsuario(self.db).mejorPokemon(numEquipo)

    def obtenerEfectos(self, nombreEspecie) :
        return gestorPokeDex.obtenerEfectos(nombreEspecie)

    def caracteristicasPokemon(self, nombreEspecie) :
        return gestorPokeDex.caracteristicasPokemon(nombreEspecie)

    def cadenaEvolutiva(self, nombreEspecie) :
        return gestorPokeDex.cadenaEvolutiva(nombreEspecie)

    def tieneAmigos(self, usuario):
        return gestorUsuario.getMyGestorUsuario(usuario).tieneAmigos()

    def mostrar_changelog(self, usuario, filtro):
        #clase de gestor_noticia por crear
        return gestorNoticias.getGestorNoticias(usuario).mostrar_changelog(usuario,filtro)

    def mostrarPokedex(self) -> str:
        return PokeDex.get_instance().mostrarPokedex()

    def mostrarInfo(self, nombreEspecie: str) -> str:
        return PokeDex.get_instance().getInfo(nombreEspecie)

    def aplicarFiltro(self, filtro: str, valor: str) -> str:
        return PokeDex.get_instance().filtrarPokedex(filtro, valor)

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

    def confirmarConContraseña(self, pNomUsuario: str, pContraseña: str) -> str:
        """
        Paso 9b: confirmarConContraseña(...) : String
        Retorna el nuevo nombre de usuario si éxito, o None si fallo.
        """
        gestor = gestorUsuario.getMyGestorUsuario(pNomUsuario, self.db)

        # Si la sesión no existe en memoria, no se puede confirmar
        if gestor is None:
            return None

        # Paso 10b: Llama al gestor y devuelve el string resultante
        return gestor.validarCredencialesYGuardarCambios(pNomUsuario, pContraseña)

    def pedirUsuariosParaAdmin(self):
        return gestorUsuario.obtenerUsuariosParaAdmin(self.db)

    def procesarAprobadoUsuario(self, pNomUsuario: str) -> bool:
        return gestorUsuario.aprobarUsuario(pNomUsuario, self.db)

    def procesarBorradoUsuario(self, pNomUsuario: str):
        return gestorUsuario.borrarUsuario(pNomUsuario, self.db)

    def procesarModificarDatosAdmin(self, pNomUsuario: str, pNombre: str, pAp: str, pNomUsuarioModif: str) -> bool:
        try:
            gestorUsuario.modificarUsuarioEnMemoriaPorAdmin(pNomUsuario, pNombre, pAp, pNomUsuarioModif, self.db)
            return True
        except Exception as e:
            print(f"Error procesarModificar: {e}")
            return False

    def buscarUsuariosConFiltro(self, pNomUsuario: str, pNomUsuarioFiltro: str):
        """
        Delega en el GestorUsuario del usuario actual.
        """
        gestor = gestorUsuario.getMyGestorUsuario(pNomUsuario, self.db)
        if gestor:
            return gestor.buscarUsuariosConFiltro(pNomUsuarioFiltro)
        return []

    def aniadirAmigo(self, pNomUsuario: str, pNomUsuarioAmigo: str) -> bool:
        """
        Delega en el GestorUsuario del usuario actual.
        """
        gestor = gestorUsuario.getMyGestorUsuario(pNomUsuario, self.db)
        if gestor:
            return gestor.aniadirAmigo(pNomUsuarioAmigo)
        return False

    @staticmethod
    def precargaInicioApp(conn):
        """
        Método estático llamado desde __init__.py al crear la BD.
        Recibe una conexión cruda de sqlite3 (no el wrapper Connection).
        """
        cursor = conn.cursor()

        # 1. Obtener datos limpios de la API
        lista_pokemons = GestorAPI.obtener_pokemons_iniciales()

        if not lista_pokemons:
            return

        print("Guardando datos en la Base de Datos...")

        # 2. Asegurar que existe la Región (Kanto) en la tabla Pokedex
        # Tu schema dice: Region TEXT PRIMARY KEY, Generacion TEXT
        cursor.execute("INSERT OR IGNORE INTO Pokedex (Region, Generacion) VALUES (?, ?)", ('Kanto', 'Primera'))

        # Queries preparadas
        sql_especie = """
                      INSERT OR IGNORE INTO EspeciePokemon
                          (Nombre, Descripcion, Legendario, AlturaMedia, PesoMedia, Region)
                      VALUES (?, ?, ?, ?, ?, ?) \
                      """

        sql_tipo = "INSERT OR IGNORE INTO Tipo (Nombre, Descripcion) VALUES (?, ?)"

        sql_especie_tipo = "INSERT OR IGNORE INTO EspecieTipo (NombreEspecie, NombreTipo) VALUES (?, ?)"

        # 3. Recorrer y guardar
        for poke in lista_pokemons:
            # A) Guardar Especie
            datos_especie = (
                poke['nombre'],
                poke['descripcion'],
                poke['legendario'],
                poke['altura'],
                poke['peso'],
                poke['region']
            )
            cursor.execute(sql_especie, datos_especie)

            # B) Guardar Tipos y Relación Especie-Tipo
            for nombre_tipo in poke['tipos']:
                # Guardamos el tipo si no existe (ej: "Fuego", "Sin descripcion por ahora")
                cursor.execute(sql_tipo, (nombre_tipo, "Tipo elemental"))

                # Relacionamos Especie con Tipo
                cursor.execute(sql_especie_tipo, (poke['nombre'], nombre_tipo))

        conn.commit()
        print(f"¡Base de datos poblada con {len(lista_pokemons)} especies nuevas!")

if __name__ == "__main__":
    pass