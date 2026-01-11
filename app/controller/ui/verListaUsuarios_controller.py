from flask import Blueprint, request, redirect, render_template, flash
from app.database.connection import Connection


def ver_lista_usuarios_blueprint(db: Connection) -> Blueprint:
    bp_verlistaus = Blueprint("ver_lista_usuarios", __name__)

    @bp_verlistaus.route("/ver_lista_usuarios")
    def ver_lista_usuarios():

        return render_template('ver_lista_usuarios.html', usuarios = ver_lista_usuarios_blueprint(db))

    return bp_verlistaus

