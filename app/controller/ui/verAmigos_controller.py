from flask import Blueprint, request, redirect, render_template, flash


def ver_amigos_blueprint():
    bp_vera = Blueprint("ver_amigos", __name__)

    @bp_vera.route("/ver_amigos")
    def lista_pokemon():
        return render_template('ver_amigos.html')

    return bp_vera