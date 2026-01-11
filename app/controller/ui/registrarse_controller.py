from flask import Blueprint, request, redirect, render_template, flash
from app.database.connection import Connection

def registrarse_blueprint(db: Connection) -> Blueprint:
    bp_registrarse = Blueprint("registrarse", __name__)

    @bp_registrarse.route("/registrarse")
    def registrarse():

        return render_template('registro.html')

    return bp_registrarse