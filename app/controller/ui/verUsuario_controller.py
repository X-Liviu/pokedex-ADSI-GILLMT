# Flask
from flask import Blueprint, render_template, request

from app.controller.model.gestorUsuario_controller import gestorUsuario
# Custom Types
from app.utils.custom_types import Custom_types

# Modelo
from app.controller.model.ranking_controller import Ranking

# Base de Datos
from app.database.connection import Connection

# Pruebas
from app.controller.model.prueba_nombre_aleatorio import generar_nombre
from app.controller.model.prueba_generar_pokemon import  get_pokemon, get_nombres

def get_info_usuario(cant: int):
    return {
        "nombre": generar_nombre(),
        "equipoEspecie": get_pokemon(cant),
        "equipoCustom": get_nombres(cant),
    }

def perfil_usuario_blueprint(db: Connection) -> Blueprint:
    nombre_direccion_ver_perfil: str = "perfil_usuario"
    bp_perfil_usuario = Blueprint(nombre_direccion_ver_perfil, __name__)

    ranking_service: Ranking = Ranking.getMyRanking(db)
    user_service: gestorUsuario = gestorUsuario.getMyGestorUsuario(db)

    @bp_perfil_usuario.route("/perfil_usuario/<name>", methods=["GET", "POST"])
    def perfil_usuario(name: str) -> str:
        """
        Usaremos el nombre dado por parametros.
        En la funcion de arriba se declarara un controlador, con
        de perfil usuario, haciendo una consulta que devuelva lo
        que nos interese de la persona seleccionada
        """

        estado_amigo_nuevo: Custom_types.VerUsuario = Custom_types.VerUsuario.NO_SOLICITADO

        if request.method == "GET":
            pass
        elif request.method == "POST" and request.form["submit_button"] == "Solicitud amistad":
            try:
                resultado_solicitud: bool = user_service.aniadirAmigo(name)

                if resultado_solicitud:
                    estado_amigo_nuevo = Custom_types.VerUsuario.AMIGO_NUEVO
                else:
                    estado_amigo_nuevo = Custom_types.VerUsuario.AMIGO_ERROR
            except:
                estado_amigo_nuevo = Custom_types.VerUsuario.AMIGO_ERROR

        return render_template("perfil_usuario.html", info_usuario = ranking_service.mostrarUsuario(name) )
        # return render_template("perfil_usuario.html", info_usuario=get_info_usuario(6), estado_solicitud = estado_amigo_nuevo)

    return bp_perfil_usuario