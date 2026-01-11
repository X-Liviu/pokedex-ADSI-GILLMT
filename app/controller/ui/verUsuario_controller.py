# Flask
from flask import Blueprint, render_template, request, session

# Custom Types
from app.model.utils.custom_types import Custom_types

# Modelo
from app.controller.model.marcoDex_controller import MarcoDex

# Base de Datos
from app.database.connection import Connection

def perfil_usuario_blueprint(db: Connection) -> Blueprint:
    nombre_direccion_ver_perfil: str = "perfil_usuario"
    bp_perfil_usuario = Blueprint(nombre_direccion_ver_perfil, __name__)

    marcodex_service: MarcoDex = MarcoDex.getMyMarcoDex(db)

    @bp_perfil_usuario.route("/perfil_usuario/<name>", methods=["GET", "POST"])
    def perfil_usuario(name: str) -> str:
        """
        Usaremos el nombre dado por parametros.
        En la funcion de arriba se declarara un controlador, con
        de perfil usuario, haciendo una consulta que devuelva lo
        que nos interese de la persona seleccionada
        """
        info_usuario = marcodex_service.mostrarUsuario("usuario", name)

        if request.method == "GET":
            pass
        elif request.method == "POST" and request.form["submit_button"] == "Solicitud amistad":
            try:
                resultado_solicitud: bool = marcodex_service.aniadirAmigo(name)

                if resultado_solicitud:
                    estado_amigo = Custom_types.VerUsuario.AMIGO_NUEVO
                else:
                    estado_amigo = Custom_types.VerUsuario.AMIGO_ERROR
            except:
                estado_amigo = Custom_types.VerUsuario.AMIGO_ERROR

        # return render_template("perfil_usuario.html", info_usuario = marcodex_service.mostrarUsuario(session['username'], name) )
        return render_template("perfil_usuario.html", info_usuario=info_usuario)

    return bp_perfil_usuario