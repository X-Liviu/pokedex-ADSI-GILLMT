import json

from flask import Blueprint, render_template, session, redirect, url_for
from app.controller.model.marcoDex_controller import MarcoDex
from app.database.connection import Connection

def detalles_equipo_blueprint(db: Connection) -> Blueprint:

    # Nombre del blueprint que usaremos en el url_for: 'ver_detalles'
    bp_detalles = Blueprint("ver_detalles", __name__)
    mDex: MarcoDex = MarcoDex.getMyMarcoDex(db)

    @bp_detalles.route("/detalles-equipo/<int:num>")
    def detalles(num: int):
        nombre_sesion = session.get('usuario')

        if not nombre_sesion:
            # --- CORRECCIÓN 2: Apuntar al blueprint correcto del login ---
            return redirect(url_for('identificacion.identificacion'))

        # Pedimos a MarcoDex la info de ese equipo concreto
        # mDex usará el nombre de usuario para buscar en su gestorUsuario
        equipo = mDex.mostrarInfoEquipo(num, nombre_sesion)

        if not equipo:
            # Si el equipo no existe o no es de ese usuario, volvemos a la lista
            return redirect(url_for('ver_equipos.ver_equipos'))

        return render_template("detalles_equipo.html",
                               equipo=equipo,
                               usuario=nombre_sesion,
                               num_equipo=num)

    return bp_detalles