from flask import Blueprint, render_template, session
from app.controller.model.marcoDex_controller import MarcoDex

def changelog_blueprint(db):
    bp_changelog = Blueprint('changelog', __name__)

    @bp_changelog.route('/changelog')
    def show_changelog():
        mDex = MarcoDex.getMyMarcoDex(db)

        if mDex.tiene_amigos():
            # PRUEBA
            if not session.get('username'):
                session['username'] = 'Horchata'

            nombreUsuario = session.get('username')

            lista_noticias = mDex.mostrar_changelog(nombreUsuario)
            return render_template('changelog.html', noticias=lista_noticias)
        else:
            return render_template('error_no_amigos.html')


    return bp_changelog