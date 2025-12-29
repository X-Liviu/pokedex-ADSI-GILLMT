from flask import Blueprint, render_template

def changelog_blueprint(db):
    # Creamos el 'plano' (blueprint) para esta parte de la web
    bp = Blueprint('changelog', __name__)

    @bp.route('/changelog')
    def show_changelog():
        # Esta función simplemente busca el HTML y lo muestra
        return render_template('changelog.html')

    return bp