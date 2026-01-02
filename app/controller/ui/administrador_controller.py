
from flask import Blueprint, request, redirect, render_template, flash

from app.database.connection import Connection
from app.controller.ui import lista_pokemon_controller
from app.controller.ui import crearEquipo_controller
from app.controller.ui import verEquipos_controller
from app.controller.ui import verAmigos_controller
from app.controller.ui import gestionarUsuarios_controller
from app.controller.ui import chatbot_controller
from app.controller.ui import verRanking_controller
from app.controller.ui import changelog_controller
from app.controller.ui import modificarDatos_controller







def lista_pokemon():
    db = Connection()
    return lista_pokemon_controller.lista_pokemon_blueprint(db)

def crear_equipo():
    db = Connection()
    return crearEquipo_controller.crear_equipo_blueprint(db)

def mis_equipos():
    db = Connection()
    return verEquipos_controller.ver_equipos_blueprint(db)

def ver_amigos():
    return verAmigos_controller.ver_amigos_blueprint()

def gestionar_usuarios():
    db = Connection()
    return gestionarUsuarios_controller.gestionar_usuarios_blueprint(db)

def chatbot():
    db = Connection()
    return chatbot_controller.chatbot_blueprint(db)

def ranking():
    db = Connection()
    return verRanking_controller.ranking_blueprint(db)

def changelog():
    db = Connection()
    return changelog_controller.changelog_blueprint(db)

def modificar_datos():
    db = Connection()
    return modificarDatos_controller.modificar_datos_blueprint(db)

