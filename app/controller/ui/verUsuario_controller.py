from flask import Blueprint, render_template
from app.database.connection import Connection

def perfil_usuario_blueprint(db: Connection) -> Blueprint:
    nombre_direccion_ver_perfil: str = "perfil_usuario"
    bp_perfil_usuario = Blueprint(nombre_direccion_ver_perfil, __name__)

    @bp_perfil_usuario.route("/perfil_usuario/<name>")
    def perfil_usuario(name: str) -> str:
        """
        Usaremos el nombre dado por parametros.
        En la funcion de arriba se declarara un controlador, con
        de perfil usuario, haciendo una consulta que devuelva lo
        que nos interese de la persona seleccionada
        """
        return render_template("perfil_usuario.html", selected_name = name)

    return bp_perfil_usuario