from flask import Blueprint, render_template, session, request
from app.controller.model.marcoDex_controller import MarcoDex

def changelog_blueprint(db):
    bp_changelog = Blueprint('changelog', __name__)

    @bp_changelog.route('/changelog')
    def show_changelog():
        mDex = MarcoDex.getMyMarcoDex(db)
        nombreUsuario = session.get('usuario')

        if mDex.tieneAmigos(nombreUsuario):

            lista_noticias = mDex.mostrar_changelog(nombreUsuario, '')
            return render_template('changelog.html', noticias=lista_noticias)
        else:
            return render_template('error_no_amigos.html')

    @bp_changelog.route('/filtro')
    def filtrar():
        mDex = MarcoDex.getMyMarcoDex(db)
        nombreUsuario = session.get('usuario')
        filtro = request.args.get('usuario')
        lista_noticias = mDex.mostrar_changelog(nombreUsuario, filtro)
        return render_template('changelog.html', noticias=lista_noticias)

    return bp_changelog