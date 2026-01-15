# Flask
from flask import Blueprint, render_template, request, session, flash, redirect

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

    @bp_perfil_usuario.route("/perfil_usuario/<otro_usuario>", methods=["GET", "POST"])
    def perfil_usuario(otro_usuario: str) -> str:
        """
        Usaremos el nombre dado por parametros.
        En la funcion de arriba se declarara un controlador, con
        de perfil usuario, haciendo una consulta que devuelva lo
        que nos interese de la persona seleccionada
        """
        usuario_actual = session.get("usuario")
        info_usuario = marcodex_service.mostrarUsuario(usuario_actual, otro_usuario)

        resultado: str = ""

        if request.method == "GET":
            resultado = render_template("perfil_usuario.html", info_usuario=info_usuario)
        if request.method == "POST" and request.form["submit_button"] == "Solicitud amistad":
            try:
                resultado_solicitud: bool = marcodex_service.aniadirAmigo(usuario_actual, otro_usuario)

                if resultado_solicitud:
                    """
                    En caso de que el proceso solicitud de amistad haya funcionado
                    correctamente, hay que actualizar la pagina, para que el usuario
                    vea que ya son amigos.
                    """
                    resultado = redirect(f"/perfil_usuario/{otro_usuario}")
            except:
                flash(f"No se pudo seguir a {otro_usuario}.")

        return resultado

    return bp_perfil_usuario