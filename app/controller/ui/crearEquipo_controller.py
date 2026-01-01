from flask import Blueprint, render_template, session, redirect, url_for
from app.controller.model.marcoDex_controller import MarcoDex
from app.database.connection import Connection


def crear_equipo_blueprint(db: Connection) -> Blueprint:
    bp_crear = Blueprint("crear_equipo", __name__)

    @bp_crear.route("/crear-equipo", methods=["GET"])
    def pantalla_crear():
        nombre_sesion = session.get('username')
        if not nombre_sesion:
            return redirect(url_for('login'))

        # Renderizamos la interfaz para elegir pokémon
        return render_template("crear_equipo.html")

    @bp_crear.route("/guardar-equipo", methods=["POST"])
    def guardar_equipo():
        # Aquí irá la lógica para salvar en la DB más adelante
        return redirect(url_for('ver_equipos.ver_equipos'))

    return bp_crear