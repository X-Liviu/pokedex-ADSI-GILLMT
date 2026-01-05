from flask import Blueprint, render_template, request

def aniadir_amigos_blueprint(db):
    bp_aniadiram = Blueprint('aniadir_amigo', __name__)

    @bp_aniadiram.route('/aniadir_amigo', methods=['GET', 'POST'])
    def aniadir_amigo():
        if request.method == 'POST':
            usuario_a_anadir = request.form.get('nombre_usuario_seleccionado')

            # TODO AÑADIR EL AMIGO EN LA BASE DE DATOS
        #PRUEBAS
        lista_usuarios = [
            {'NombreUsuario': 'Machaca2000', 'nombre': 'Liviu', 'apellido':  'Deleanu', 'es_amigo': False},
            {'NombreUsuario': 'Palanquin123', 'nombre': 'Iker', 'apellido': 'Ciordia', 'es_amigo': True},
            {'NombreUsuario': 'Iturri', 'nombre': 'Iker', 'apellido': 'Fuente', 'es_amigo': False}

        ]

        return render_template("aniadir_amigo.html", usuarios = lista_usuarios)

    return bp_aniadiram