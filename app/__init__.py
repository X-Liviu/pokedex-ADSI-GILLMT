import os.path
import sqlite3

from flask import Flask

# MAEs
from app.controller.model.marcoDex_controller import MarcoDex
from app.controller.model.ranking_controller import Ranking

# Custom UI
from app.controller.ui.verRanking_controller import ranking_blueprint

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


def inicializar_MAEs(db: Connection) -> None:
    """
    En vez de realizar las inicializaciones cuando se quiera
    acceder al objeto MAE. Inicializamos aqui los objetos. Asi
    nos aseguramos que siempre que se hace un getMiObjeto exista
    la instancia.
    """
    Ranking(db)
    MarcoDex(db)

def init_db():
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

    inicializar_MAEs(db)

    """
    app.register_blueprint(user_blueprint(db))
    app.register_blueprint(book_blueprint(db))
    app.register_blueprint(loan_blueprint(db))
    """

    app.register_blueprint(ranking_blueprint(db))

    """
    Esto es para que se redireccione a otra
    direccion, siempre que se quiera acceder
    a index.
    """

    @app.route('/')
    def index() -> str:
        return app.redirect("/ranking")

    return app