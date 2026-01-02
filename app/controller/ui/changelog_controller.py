from flask import Blueprint, render_template

def changelog_blueprint(db):
    bp_changelog = Blueprint('changelog', __name__)

    @bp_changelog.route('/changelog')
    def show_changelog():
        # Esta función simplemente busca el HTML y lo muestra
        return render_template('changelog.html')

    return bp_changelog