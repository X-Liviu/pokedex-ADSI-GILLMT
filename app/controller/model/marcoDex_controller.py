import string

from app.controller.model.chatbot_controller import ChatBot
from app.controller.model.gestorEfectos_controller import gestorEfectos
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

    def mostrarRanking(self) -> Custom_types.Ranking.JSONRanking:
        return Ranking.getMyRanking(self.db).mostrarRanking()

    def mostrarUsuario(self, pNombreUsuario: str, pNombreAmigo: str) -> Custom_types.Ranking.JSONRankingUsuario:
        return Ranking.getMyRanking(self.db).mostrarUsuario(pNombreUsuario, pNombreAmigo)

    def aniadirAmigo(self, nombreUsuario: str, nombreAmigo: str) -> Custom_types.GestorUsuario.JSONEstadoAmigo:
        resultado: Custom_types.GestorUsuario.EstadoAmigo = {"Aniadido": False}
        resultado["Aniadido"] = gestorUsuario.getMyGestorUsuario(nombreUsuario, self.db).aniadirAmigo(nombreAmigo)
        return resultado

    #DE LIVIU
    def aniadirAmigo(self, pNomUsuario: str, pNomUsuarioAmigo: str) -> bool:
        """
        Delega en el GestorUsuario del usuario actual.
        """
        gestor = gestorUsuario.getMyGestorUsuario(pNomUsuario, self.db)
        if gestor:
            return gestor.aniadirAmigo(pNomUsuarioAmigo)
        return False

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
        return ChatBot.getChatBot().mostrarOpciones()

    def mejorPokemon(self, nombre_usuario, numEquipo):
        return gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db).mejorPokemon(numEquipo)

    def obtenerEfectos(self, nombreEspecie) :
        return PokeDex.get_instance().obtenerEfectos(nombreEspecie)

    def caracteristicasPokemon(self, nombreEspecie) :
        return PokeDex.get_instance().caracteristicasPokemon(nombreEspecie)

    def cadenaEvolutiva(self, nombreEspecie) :
        return PokeDex.get_instance().cadenaEvolutiva(nombreEspecie)

    def tieneAmigos(self, usuario):
        return gestorUsuario.getMyGestorUsuario(usuario).tieneAmigos()

    def mostrar_changelog(self, usuario, filtro, db):
        return gestorNoticias.getGestorNoticias(db).mostrar_changelog(usuario,filtro, db)

    def mostrarPokedex(self) -> str:
        return PokeDex.get_instance().mostrarPokedex()

    def mostrarInfo(self, nombreEspecie: str) -> str:
        return PokeDex.get_instance().getInfo(nombreEspecie)

    def aplicarFiltro(self, filtro: str, valor: str) -> str:
        return PokeDex.get_instance().filtrarPokedex(filtro, valor)

    def iniciarSesion(self, pNomUsuario: str, pContrasena: str) -> bool:
        """
        Paso 2: iniciarSesion
        Orquesta el login y la precarga de datos (Globales y del Usuario).
        """
        # Paso 3: Llamada al Gestor
        exito = gestorUsuario.iniciarSesion(pNomUsuario, pContrasena, self.db)

        if exito:
            # Paso 14aa: Cargar datos globales (Pokedex)
            # Respetamos que precargarDatos() sea void y sin argumentos.
            self.precargarDatos()
            # Recuperamos el gestor del usuario actual para cargar sus datos privados
            gestor = gestorUsuario.getMyGestorUsuario(pNomUsuario, self.db)
            if gestor:
                print("hay gestor")
                gestor.precargarEquipos()
                gestor.precargarAmigos()

        return exito

    def precargarDatos(self):
        """
        Paso 14aa: precargarDatos() : void
        Carga exclusivamente la información global (La Pokedex).
        """
        # Paso 15aa: Consulta a BD para EspeciePokemon
        sql = "SELECT * FROM EspeciePokemon"

        resultado = self.db.select(sql, ())  # Pasos 16aa

        mi_pokedex = PokeDex.get_instance()
        mi_pokedex.reiniciarPokedex()
        # Paso 17aa: Recorrer resultados
        for fila in resultado:
            # Pasos 18aa - 23aa: Obtener datos
            nomPokemon = fila['Nombre']
            descr = fila['Descripcion']
            legendario = bool(fila['Legendario'])
            altMedia = float(fila['AlturaMedia'])
            pesoMedio = float(fila['PesoMedia'])
            region = fila['Region']

            # Paso 15aa: Consulta a BD para los tipos del Pokémon
            sql = "SELECT NombreTipo FROM EspecieTipo WHERE NombreEspecie = '%s'" % nomPokemon

            resultado = self.db.select(sql, ())  # Pasos 16aa
            tipos = []
            for fila in resultado:
                tipos.append(fila['NombreTipo'])


            # Paso 15aa: Consulta a BD para las evoluciones
            sql = "SELECT Evolucion FROM Evolucion WHERE Preevolucion = '%s'" % nomPokemon

            resultado = self.db.select(sql, ())  # Pasos 16aa
            evoluciones = []
            for fila in resultado:
                evoluciones.append(fila['Evolucion'])

            # Paso 15aa: Consulta a BD para las preevoluciones
            sql = "SELECT Preevolucion FROM Evolucion WHERE Evolucion = '%s'" % nomPokemon

            resultado = self.db.select(sql, ())  # Pasos 16aa
            preevoluciones = []
            for fila in resultado:
                preevoluciones.append(fila['Preevolucion'])

            # Paso 24aa y 25aa: Añadir a Pokedex
            mi_pokedex.añadirPokemon(nomPokemon, descr, legendario, altMedia, pesoMedio, tipos, evoluciones, preevoluciones, region)
        # Paso 15aa: Efectos
        sql = "SELECT * FROM EfectoTipo"
        resultado = self.db.select(sql, ())  # Pasos 16aa
        gEfectos = gestorEfectos.getGestorEfectos()
        for fila in resultado:
            # Pasos 18aa - 23aa: Obtener datos
            tipoAtac = fila['NombreTipoAtac']
            tipoDef = fila['NombreTipoDef']
            efecto = fila['Efecto']
            gEfectos.anadirEfecto(tipoAtac, tipoDef, efecto)

        print(f"[DEBUG] Precarga global finalizada: {len(mi_pokedex.listaEspecies)} especies en Pokedex.")

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



    @staticmethod
    def precargaInicioApp(conn):
        """
        Método estático llamado desde __init__.py al crear la BD.
        """
        cursor = conn.cursor()

        # 1. Obtener datos limpios de la API
        lista_tipos = GestorAPI.cargarTiposEfectos()
        lista_pokemons = GestorAPI.cargarPokemons()

        if not lista_pokemons:
            return

        print("Guardando datos en la Base de Datos...")

        # Queries preparadas
        sql_especie = """
                      INSERT OR IGNORE INTO EspeciePokemon
                          (Nombre, Descripcion, Legendario, AlturaMedia, PesoMedia, Region)
                      VALUES (?, ?, ?, ?, ?, ?) \
                      """

        sql_tipo = "INSERT OR IGNORE INTO Tipo (Nombre, Descripcion) VALUES (?, ?)"

        sql_especie_tipo = "INSERT OR IGNORE INTO EspecieTipo (NombreEspecie, NombreTipo) VALUES (?, ?)"

        sql_evolucion = "INSERT OR IGNORE INTO Evolucion VALUES (?, ?)"

        sql_efecto= "INSERT OR IGNORE INTO EfectoTipo VALUES (?, ?, ?)"

        #Cargamos todos los tipos
        for tipo in lista_tipos:
            cursor.execute(sql_tipo, (tipo['nombre'], tipo['descripcion']))

        #Cargamos los efectos
        for tipo in lista_tipos:
            nombre = tipo['nombre']
            eficaz = tipo['eficaz']
            for t in eficaz:
                cursor.execute(sql_efecto, (nombre, t, 'Eficaz'))
            debil = tipo['debil']
            for t in debil:
                cursor.execute(sql_efecto, (nombre, t, 'Débil'))
            sin_efecto = tipo['sin_efecto']
            for t in sin_efecto:
                cursor.execute(sql_efecto, (nombre, t, 'Sin efecto'))

        print(f"¡Tipos y efectos cargados correctamente!")

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
                # Relacionamos Especie con Tipo
                cursor.execute(sql_especie_tipo, (poke['nombre'], nombre_tipo))

        for poke in lista_pokemons:
            # C) Guardar Evoluciones y Preevoluciones
            for evolucion in poke['evoluciones']:
                # Guardamos el tipo si no existe (ej: "Fuego", "Sin descripcion por ahora")
                cursor.execute(sql_evolucion, (evolucion, poke['nombre']))
            for preevolucion in poke['preevoluciones']:
                # Guardamos el tipo si no existe (ej: "Fuego", "Sin descripcion por ahora")
                cursor.execute(sql_evolucion, (poke['nombre'], preevolucion))


        conn.commit()
        print(f"¡Base de datos poblada con {len(lista_pokemons)} especies nuevas!")

    def obtenerListaAmigos(self, nombre_usuario: str):
        """
        Necesario para el paso 2 (Ver Amigos) del flujo general.
        """
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario, self.db)
        if gestor:
            return gestor.obtenerListaAmigos()
        return []

    def procesarBorradoAmigo(self, pNomUsuarioAmigo: str, nombre_usuario_actual: str):
        """
        Paso 4 del flujo.
        Delega en el GestorUsuario y retorna la lista actualizada.
        """
        gestor = gestorUsuario.getMyGestorUsuario(nombre_usuario_actual, self.db)
        if gestor:
            return gestor.borrarAmigo(pNomUsuarioAmigo)
        return []

if __name__ == "__main__":
    pass