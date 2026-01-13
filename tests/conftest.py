import pytest
import os
import sqlite3

from flask import Flask, session, redirect, url_for, make_response

# MAEs
from app.controller.model.marcoDex_controller import MarcoDex
from app.controller.model.gestorUsuario_controller import gestorUsuario

# Custom UI
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
from app.controller.ui.confirmarContrasena_controller import confirmar_contrasena_blueprint
from app.controller.ui.verListaUsuarios_controller import ver_lista_usuarios_blueprint
from app.controller.ui import menu_principal_controller

# Se especifican las rutas que estan en root, no queremos que el directorio tests sea root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATES_DIR = os.path.join(ROOT_DIR, "app", "templates")
STATIC_DIR = os.path.join(ROOT_DIR, "app", "static")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    DB_PATH = os.path.join(BASE_DIR, "ranking_test.sqlite")
    SECRET_KEY = "test_ranking"

class Connection:

    def __init__(self):
        self.connection = sqlite3.connect(
            Config.DB_PATH,
            check_same_thread=False
        )
        self.connection.row_factory = sqlite3.Row
        self.__initialized = True


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

        # ESTO ES LO QUE FALTA: Capturamos el ID generado
        last_id = cursor.lastrowid

        cursor.close()
        return last_id  # Devolvemos el ID para usarlo en las otras tablas

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


def init_db():
    """
    Importa la estructura del archivo .sql
    SOLO si la base de datos no existe aun.
    """
    print("Verificando base de datos...")

    # Si el archivo NO existe, lo creamos
    if not os.path.exists(Config.DB_PATH):
        print("No se encontró base de datos. Creando nueva desde schema.sql...")
        conn = sqlite3.connect(Config.DB_PATH)

        try:
            # 1. Crear las tablas
            with open('app/database/schema.sql', encoding='utf-8') as f:
                conn.executescript(f.read())

            # 2. CARGA AUTOMÁTICA DE LA API
            # Pasamos la conexión para que MarcoDex la use antes de cerrarla
            print("Tablas creadas. Llamando a MarcoDex para poblar datos...")
            MarcoDex.precargaInicioApp(conn)

            print("Base de datos creada e inicializada exitosamente.")

        except Exception as e:
            print(f"Error crítico inicializando BD: {e}")
        finally:
            conn.close()
    else:
        # Si YA existe, no hacemos nada para no borrar los datos
        print("La base de datos ya existe. Iniciando sin sobrescribir.")

@pytest.fixture()
def create_app():
    app = Flask(__name__,
                template_folder=TEMPLATES_DIR,
                static_folder=STATIC_DIR
    )
    app.config.from_object(Config)

    app.config['PROPAGATE_EXCEPTIONS'] = True

    # Inicializar base de datos
    init_db()

    # Crear conexión a la base de datos (Objeto Connection wrapper)
    db = Connection()

    # Blueprints
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

    @app.route('/')
    def index():
        # 1. Protección de ruta (Si no hay usuario, fuera)
        if 'usuario' not in session:
            return redirect(url_for('identificacion.identificacion'))

        if gestorUsuario.getMyGestorUsuario(session['usuario']) is None:
            gestorUsuario.cargarUsuario(session['usuario'], db)

        # 2. Generamos el HTML del menú
        html_content = menu_principal_controller.mostrar_menu()

        # Evitar caché del navegador
        respuesta = make_response(html_content)
        respuesta.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        respuesta.headers["Pragma"] = "no-cache"
        respuesta.headers["Expires"] = "0"

        return respuesta

    yield app

@pytest.fixture()
def client(create_app):
    return create_app.test_client()