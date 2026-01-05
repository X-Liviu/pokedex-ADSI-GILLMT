from flask import Blueprint, render_template
from app.database.connection import Connection

def changelog_blueprint(db):
    bp_changelog = Blueprint('changelog', __name__)

    @bp_changelog.route('/changelog')
    def show_changelog():
        lista_noticias = [{'NombreUsuario': 'Machaca2000', 'FechaHora': '2026-01-05 14:30:00', 'contenido': 'Equipo de fuego terminado 🔥🔥🔥'},
                    {'NombreUsuario': 'Sopórifero2', 'FechaHora': '2025-03-15 16:42:00', 'contenido': 'Pikachu capturado'}
                    ]
        return render_template('changelog.html', noticias= lista_noticias)

    return bp_changelog