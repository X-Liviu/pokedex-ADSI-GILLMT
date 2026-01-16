import pytest
import os
import sqlite3
from flask import Flask, session, redirect, url_for

# MAEs
from app.controller.model.marcoDex_controller import MarcoDex
from app.controller.model.gestorUsuario_controller import gestorUsuario
from app.controller.model.ranking_controller import Ranking

# Blueprints
from app.controller.ui.chatbot_controller import chatbot_blueprint
from app.controller.ui.verRanking_controller import ranking_blueprint
from app.controller.ui.changelog_controller import changelog_blueprint
from app.controller.ui.verEquipos_controller import ver_equipos_blueprint
from app.controller.ui.detallesEquipo_controller import detalles_equipo_blueprint
from app.controller.ui.crearEquipo_controller import crear_equipo_blueprint
from app.controller.ui.lista_pokemon_controller import lista_pokemon_blueprint
from app.controller.ui.modificar_equipo_controller import modificar_equipo_blueprint
from app.controller.ui.verAmigos_controller import ver_amigos_blueprint
from app.controller.ui.modificarDatos_controller import modificar_datos_blueprint
from app.controller.ui.identificacion_controller import identificacion_blueprint
from app.controller.ui.registrarse_controller import registrarse_blueprint
from app.controller.ui.verListaUsuarios_controller import ver_lista_usuarios_blueprint
from app.controller.ui.confirmarContrasena_controller import confirmar_contrasena_blueprint
from app.controller.ui.menu_principal_controller import menu_principal_blueprint

# Rutas
PROJECT_ROOT = os.getcwd()
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "app", "templates")
STATIC_DIR = os.path.join(PROJECT_ROOT, "app", "static")
# Usamos un nombre fijo para la BD de test. NO LA BORRAREMOS si ya tiene datos.
DB_PATH = os.path.join(PROJECT_ROOT, "dbtest.sqlite")

# Usuarios originales del schema.sql que NO debemos borrar
SEED_USERS = [
    'LiviuX', 'TataX', 'GorkaX', 'LauraX', 'MarcoX', 'IkerX',
    'AshKetchum', 'GaryOak', 'Misty', 'Brock'
]


class Config:
    DB_PATH = DB_PATH
    SECRET_KEY = "test_ranking"
    TESTING = True


class Connection:
    def __init__(self):
        self.connection = sqlite3.connect(Config.DB_PATH, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        # Activamos Foreign Keys para que funcione el ON DELETE CASCADE si existe
        self.connection.execute("PRAGMA foreign_keys = ON")

    def execute(self, sentence, parameters=None):
        cursor = self.connection.cursor()
        if parameters:
            cursor.execute(sentence, parameters)
        else:
            cursor.execute(sentence)
        self.connection.commit()
        return cursor

    def select(self, sentence, parameters=None):
        cursor = self.connection.cursor()
        if parameters:
            cursor.execute(sentence, parameters)
        else:
            cursor.execute(sentence)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def insert(self, sentence, parameters=None):
        cursor = self.connection.cursor()
        if parameters:
            cursor.execute(sentence, parameters)
        else:
            cursor.execute(sentence)
        self.connection.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id

    def update(self, sentence, parameters=None):
        cursor = self.connection.cursor()
        if parameters:
            cursor.execute(sentence, parameters)
        else:
            cursor.execute(sentence)
        self.connection.commit()
        cursor.close()

    def delete(self, sentence, parameters=None):
        cursor = self.connection.cursor()
        if parameters:
            cursor.execute(sentence, parameters)
        else:
            cursor.execute(sentence)
        self.connection.commit()
        cursor.close()

    def close(self):
        self.connection.close()


@pytest.fixture(scope="session")
def setup_database_once():
    """
    Esta fixture se ejecuta UNA SOLA VEZ por toda la sesión de pruebas.
    Se encarga de crear la BD y cargar la API solo si no existe.
    """
    if os.path.exists(Config.DB_PATH):
        print("\n[INFO] Base de datos encontrada. Usando caché (NO se descarga API).")
        return

    print("\n[INFO] Creando Base de Datos desde cero y descargando API...")
    conn = sqlite3.connect(Config.DB_PATH)
    try:
        schema_path = os.path.join(PROJECT_ROOT, 'app', 'database', 'schema.sql')
        with open(schema_path, encoding='utf-8') as f:
            conn.executescript(f.read())

        # Carga de la API (Esto es lo lento)
        MarcoDex.precargaInicioApp(conn)
        print("[INFO] Carga inicial completada.")
    except Exception as e:
        print(f"[ERROR] Fallo inicializando BD: {e}")
        # Si falla, borramos el archivo corrupto
        conn.close()
        if os.path.exists(Config.DB_PATH):
            os.remove(Config.DB_PATH)
        raise e
    finally:
        conn.close()


@pytest.fixture()
def create_app(setup_database_once):
    """
    Esta fixture se ejecuta POR CADA TEST.
    Crea la app, conecta a la BD existente y limpia los datos al terminar.
    """
    # 1. Limpieza de memoria (Singletons)
    MarcoDex.myMarcoDex = None
    Ranking.myRanking = None # Lo necesito hacer para que mi test funcione
    gestorUsuario._instancias_usuarios = {}
    gestorUsuario.listaUsuariosParaAdmin = []

    app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
    app.config.from_object(Config)

    db = Connection()

    # Registro de Blueprints
    app.register_blueprint(ranking_blueprint(db))
    app.register_blueprint(ver_equipos_blueprint(db))
    app.register_blueprint(detalles_equipo_blueprint(db))
    app.register_blueprint(crear_equipo_blueprint(db))
    app.register_blueprint(changelog_blueprint(db))
    app.register_blueprint(lista_pokemon_blueprint(db))
    app.register_blueprint(chatbot_blueprint(db))
    app.register_blueprint(modificar_equipo_blueprint(db))
    app.register_blueprint(modificar_datos_blueprint(db))
    app.register_blueprint(ver_amigos_blueprint(db))
    app.register_blueprint(identificacion_blueprint(db))
    app.register_blueprint(registrarse_blueprint(db))
    app.register_blueprint(ver_lista_usuarios_blueprint(db))
    app.register_blueprint(confirmar_contrasena_blueprint(db))
    app.register_blueprint(menu_principal_blueprint(db))

    @app.route('/')
    def index():
        session.clear()
        return redirect(url_for('identificacion.identificacion'))

    # Entrega la app al test
    yield app

    # --- TEARDOWN (Limpieza después del test) ---
    # Borramos cualquier usuario que NO esté en la lista original (SEED_USERS)
    # Esto elimina 'NuevoUser123', 'Impostor', etc., dejando la BD lista para el siguiente test.

    placeholders = ','.join(['?'] * len(SEED_USERS))

    try:
        # Borramos primero de tablas dependientes por si acaso no hay CASCADE
        # 1. Equipos de usuarios nuevos
        db.execute(f"DELETE FROM Equipo WHERE NombreUsuario NOT IN ({placeholders})", tuple(SEED_USERS))
        # 2. Publicaciones de usuarios nuevos
        db.execute(f"DELETE FROM Publica WHERE NombreUsuario NOT IN ({placeholders})", tuple(SEED_USERS))
        # 3. Finalmente el Usuario
        db.execute(f"DELETE FROM Usuario WHERE NombreUsuario NOT IN ({placeholders})", tuple(SEED_USERS))

        # 1. Borramos la relación intermedia de los equipos de TataX
        db.execute("""
                   DELETE
                   FROM PokemonEnEquipo
                   WHERE idEquipoInterno IN (SELECT idEquipo FROM Equipo WHERE NombreUsuario = 'TataX')
                   """)

        # 2. Borramos los ejemplares de Pokemon de TataX
        db.execute("""
                   DELETE
                   FROM Pokemon
                   WHERE idPokemon IN (SELECT idPokemon
                                       FROM PokemonEnEquipo
                                       WHERE idEquipoInterno IN
                                             (SELECT idEquipo FROM Equipo WHERE NombreUsuario = 'TataX'))
                   """)

        # 3. Borramos los equipos de TataX
        db.execute("DELETE FROM Equipo WHERE NombreUsuario = 'TataX'")
        db.execute("DELETE FROM Publica WHERE NombreUsuario = 'TataX'")

        # print("Limpieza de BD realizada correctamente.")
    except Exception as e:
        print(f"Error en limpieza de BD: {e}")

    db.close()


@pytest.fixture()
def client(create_app):
    return create_app.test_client()