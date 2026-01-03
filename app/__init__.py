import os.path
import sqlite3

from flask import Flask

from app.controller.model.gestorUsuario_controller import gestorUsuario
# MAEs
from app.controller.model.marcoDex_controller import MarcoDex
from app.controller.model.ranking_controller import Ranking
from app.model.usuario import Usuario
from app.controller.model.especie_controller import Especie
from app.controller.model.tipo_controller import Tipo
from app.controller.model.pokeDex_controller import PokeDex

# Custom UI
from app.controller.ui.verRanking_controller import ranking_blueprint
from app.controller.ui.changelog_controller import changelog_blueprint
from app.controller.ui.verEquipos_controller import ver_equipos_blueprint
from app.controller.ui.detallesEquipo_controller import detalles_equipo_blueprint
from app.controller.ui.crearEquipo_controller import crear_equipo_blueprint
from app.controller.ui.lista_pokemon_controller import lista_pokemon_blueprint

# Tipos de datos
from config import Config

# UIs de Janire
from app.controller.ui.book_controller import book_blueprint
from app.controller.ui.loan_controller import loan_blueprint
from app.controller.ui.user_controlller import user_blueprint

# Base de datos
from app.database.connection import Connection


"""
POR QUE ESTE NOMBRE ?
Para poder importar codigo en Python que se encuentra en una carpeta,
hace falta que el directorio contenga un archivo .py, cuyo nombre sea
__init__.py. Ademas a la hora de importar codigo de la carpeta, se puede
programar dentro del archivo __init__.py, haciendo que el directorio, ademas
de las funciones de los otros archivos mediante directoio.archivo, pueda acceder
a funciones implementadas aqui, como si la carpeta fuera un archivo.py.
"""

def init_db():
    """
    Importa la estructura del archivo .sql
    a la base de datos (marcoDex.sqlite)
    """
    print("Iniciando la base de datos")
    if os.path.exists(Config.DB_PATH):
        print("La base de datos existe")
        conn = sqlite3.connect(Config.DB_PATH)
        with open('app/database/schema.sql') as f:
            conn.executescript(f.read())
        conn.close()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar base de datos
    init_db()

    # Crear conexión a la base de datos
    db = Connection()

    ## --- DATOS DE PRUEBA (MOCK) ---
    ## Creamos un par de tipos
    #t_fuego = Tipo("Fuego","es fueguito")
    #t_planta = Tipo("Planta", "es plantita")
    #t_elec = Tipo("Electrico", "es electrico")
    ## Creamos un par de especies según tu constructor
    ## (nombre, descripcion, legendario, altura, peso, tipos, region)
    #p1 = Especie("Bulbasaur", "Un Pokémon semilla.", False, 0.7, 6.9, ["latigo cepa"], [t_planta])
    #p2 = Especie("Charmander", "Prefiere las cosas calientes.", False, 0.6, 8.5, ["lanzallamas"], [t_fuego])
    #p3 = Especie("Pikachu", "Ratón eléctrico.", False, 0.4, 6.0, ["impactrueno"], [t_elec])

    ## Inicializamos el Singleton con esta lista
    #PokeDex.get_instance([p1, p2, p3])
    ## ------------------------------

    """
    app.register_blueprint(user_blueprint(db))
    app.register_blueprint(book_blueprint(db))
    app.register_blueprint(loan_blueprint(db))
    """

    app.register_blueprint(ranking_blueprint(db))
    app.register_blueprint(ver_equipos_blueprint(db))
    app.register_blueprint(detalles_equipo_blueprint(db))
    app.register_blueprint(crear_equipo_blueprint(db))
    app.register_blueprint(changelog_blueprint(db))
    app.register_blueprint(lista_pokemon_blueprint(db))

    """
    Esto es para que se redireccione a otra
    direccion, siempre que se quiera acceder
    a index.
    """

    @app.route('/')
    def index() -> str:
        return app.redirect("/lista_pokemon")

    return app