from flask import Blueprint, request, redirect, render_template, flash
from app.database.connection import Connection


def gestionar_usuarios_blueprint(db: Connection) -> Blueprint:
    bp_gestionarus = Blueprint("gestionar_usuarios", __name__)

    @bp_gestionarus.route("/gestionar_usuarios")
    def gestionar_usuarios():

        return render_template('gestionar_usuarios.html', usuarios = gestionar_usuarios_blueprint(db))

    return bp_gestionarus

