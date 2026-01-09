from flask import Blueprint, render_template, request

def aniadir_amigos_blueprint(db):
    bp_aniadiram = Blueprint('aniadir_amigo', __name__)

    @bp_aniadiram.route('/aniadir_amigo', methods=['GET', 'POST'])
    def aniadir_amigo():
        if request.method == 'POST':
            usuario_a_anadir = request.form.get('nombre_usuario_seleccionado')

            # TODO AÑADIR EL AMIGO EN LA BASE DE DATOS

        return render_template("aniadir_amigo.html", usuarios = ...)

    return bp_aniadiram