from flask import Blueprint, request, redirect, render_template, flash
from app.database.connection import Connection


def lista_pokemon_blueprint(db: Connection) -> Blueprint:
    bp_listap = Blueprint("lista_pokemon", __name__)

    @bp_listap.route("/lista_pokemon")
    def lista_pokemon():

        return render_template('lista_pokemon.html')

    return bp_listap