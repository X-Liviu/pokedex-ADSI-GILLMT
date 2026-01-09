from flask import Blueprint, render_template
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex

def changelog_blueprint(db):
    bp_changelog = Blueprint('changelog', __name__)

    @bp_changelog.route('/changelog')
    def show_changelog():
        mDex = MarcoDex.getMyMarcoDex(db)

        if mDex.tiene_amigos():

            nombreUsuario = mDex.getNombreUsuario()
            lista_noticias = mDex.mostrar_changelog(nombreUsuario)
            return render_template('changelog.html', noticias=lista_noticias)
        else:
            return render_template('error_no_amigos.html')


    return bp_changelog