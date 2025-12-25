from flask import Blueprint, render_template

from app.controller.model.marcoDex_controller import MarcoDex
from app.database.connection import Connection

from app.controller.model.prueba_nombre_aleatorio import generar_nombre
from app.controller.model.prueba_generar_pokemon import  get_pokemon, get_nombres

def get_info_usuario(cant: int):
    resultado = {
        "nombre": generar_nombre(),
        "equipoEspecie": get_pokemon(cant),
        "equipoCustom": get_nombres(cant),
    }

    return resultado

def perfil_usuario_blueprint(db: Connection) -> Blueprint:
    nombre_direccion_ver_perfil: str = "perfil_usuario"
    bp_perfil_usuario = Blueprint(nombre_direccion_ver_perfil, __name__)

    ranking_service: MarcoDex = MarcoDex.getMyMarcoDex()

    @bp_perfil_usuario.route("/perfil_usuario/<name>")
    def perfil_usuario(name: str) -> str:
        """
        Usaremos el nombre dado por parametros.
        En la funcion de arriba se declarara un controlador, con
        de perfil usuario, haciendo una consulta que devuelva lo
        que nos interese de la persona seleccionada
        """
        # return render_template("perfil_usuario.html", info_usuario = ranking_service.mostrarUsuario(name) )
        return render_template("perfil_usuario.html", info_usuario=get_info_usuario(6))

    return bp_perfil_usuario