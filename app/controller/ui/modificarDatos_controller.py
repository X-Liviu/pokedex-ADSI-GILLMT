from flask import Blueprint, request, redirect, render_template, flash
from app.database.connection import Connection


def modificar_datos_blueprint(db: Connection) -> Blueprint:
    bp_modificardat = Blueprint("modificar_datos", __name__)

    @bp_modificardat.route("/modificar_datos")
    def modificar_datos():

        return render_template('modificar_datos.html')

    return bp_modificardat