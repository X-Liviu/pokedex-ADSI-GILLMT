from flask import Blueprint, request, redirect, render_template, flash
# Importamos Connection para que sepa qué es 'db' (opcional, pero buena práctica)
from app.database.connection import Connection

# 1. AÑADIDO 'db' en los paréntesis para arreglar el TypeError
def ver_amigos_blueprint(db: Connection):
    bp_vera = Blueprint("ver_amigos", __name__)

    @bp_vera.route("/ver_amigos")
    # 2. CAMBIADO el nombre de la función a 'ver_amigos' para arreglar el enlace del HTML
    def ver_amigos():
        # Aquí en el futuro usarás 'db' para buscar los amigos reales
        return render_template('ver_amigos.html')

    return bp_vera