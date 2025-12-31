# Flask y herramientas
from flask import Blueprint, render_template, session, redirect, url_for

# Tus clases y tipos
from app.controller.model.marcoDex_controller import MarcoDex
from app.database.connection import Connection

def ver_equipos_blueprint(db: Connection) -> Blueprint:
    nombre_direccion_ver_equipos: str = "ver_equipos"
    bp_ver_equipos = Blueprint(nombre_direccion_ver_equipos, __name__)

    # Obtenemos la instancia de MarcoDex
    mDex: MarcoDex = MarcoDex.getMyMarcoDex(db)

    @bp_ver_equipos.route("/mis-equipos", methods=["GET"])
    def ver_equipos(): # Quitamos el -> str porque redirect devuelve un objeto 'Response'
        # 1. Identificamos al usuario
        nombre_sesion = session.get('username')

        if not nombre_sesion:
            return redirect(url_for('login')) # Redirección si no hay sesión

        # 2. Comprobamos si tiene equipos
        if not mDex.tieneEquipos(nombre_sesion):
            return render_template("error_no_equipos.html", nombre=nombre_sesion)

        # 3. Cargamos la lista
        lista_equipos = mDex.getListaEquipos(nombre_sesion)

        # 4. Renderizamos
        return render_template("mis_equipos.html",
                               usuario_nombre=nombre_sesion,
                               equipos=lista_equipos)

    return bp_ver_equipos