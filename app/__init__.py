import os.path
import sqlite3

from flask import Flask, session, redirect, url_for, make_response

from app.controller.model.gestorUsuario_controller import gestorUsuario
# MAEs
from app.controller.model.marcoDex_controller import MarcoDex
from app.controller.model.ranking_controller import Ranking
from app.controller.ui.chatbot_controller import chatbot_blueprint
from app.model.usuario import Usuario
from app.controller.model.especie_controller import Especie
from app.controller.model.tipo_controller import Tipo
from app.controller.model.pokeDex_controller import PokeDex

# Custom UI
from app.controller.ui import menu_principal_controller
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
# Tipos de datos
from config import Config

# UIs de Janire
from app.controller.ui.book_controller import book_blueprint
from app.controller.ui.loan_controller import loan_blueprint
from app.controller.ui.user_controlller import user_blueprint

# Base de datos
from app.database.connection import Connection


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
        with open('app/database/schema.sql', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.close()
        print("Base de datos creada exitosamente.")
    else:
        # Si YA existe, no hacemos nada para no borrar los datos
        print("La base de datos ya existe. Iniciando sin sobrescribir.")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar base de datos
    init_db()

    # Crear conexión a la base de datos
    db = Connection()

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

    """
    Esto es para que se redireccione a otra
    direccion, siempre que se quiera acceder
    a index.
    """

    @app.route('/')
    def index():
        # 1. Protección de ruta (Si no hay usuario, fuera)
        if 'usuario' not in session:
            return redirect(url_for('identificacion.identificacion'))
        else:
            gestorUsuario.cargarUsuario(session['usuario'], db) #cargar el usuario en gestorUsuario

        # 2. Generamos el HTML del menú
        html_content = menu_principal_controller.mostrar_menu()

        # --- CAMBIO 2: Evitar caché del navegador ---
        respuesta = make_response(html_content)
        respuesta.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        respuesta.headers["Pragma"] = "no-cache"
        respuesta.headers["Expires"] = "0"

        return respuesta

    return app