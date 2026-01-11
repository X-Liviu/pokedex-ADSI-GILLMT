from flask import Blueprint, render_template, session, redirect, url_for
from app.controller.model.marcoDex_controller import MarcoDex
from app.database.connection import Connection

def ver_equipos_blueprint(db: Connection) -> Blueprint:
    nombre_direccion_ver_equipos: str = "ver_equipos"
    bp_ver_equipos = Blueprint(nombre_direccion_ver_equipos, __name__)

    # Obtenemos la instancia de MarcoDex
    mDex: MarcoDex = MarcoDex.getMyMarcoDex(db)

    @bp_ver_equipos.route("/mis-equipos", methods=["GET"])
    def ver_equipos():
        nombre_sesion = session.get('usuario')

        if not nombre_sesion:
            return redirect(url_for('identificacion.identificacion'))

        if not mDex.tieneEquipos(nombre_sesion):
            return render_template("error_no_equipos.html", nombre=nombre_sesion)

        datos = mDex.getListaEquipos(nombre_sesion)

        return render_template("mis_equipos.html",
                               usuario_nombre=nombre_sesion,
                               equipos=datos["equipos"])

    return bp_ver_equipos