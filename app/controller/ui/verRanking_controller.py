from flask import Blueprint, request, redirect, render_template, flash, url_for

from app.controller.model.ranking_controller import Ranking
from app.database.connection import Connection
from app.controller.ui.verUsuario_controller import perfil_usuario_blueprint

def ranking_blueprint(db: Connection) -> Blueprint:
    nombre_direccion_ranking: str = "ranking"
    bp_ranking = Blueprint(nombre_direccion_ranking, __name__)

    # nombre_direccion_ver_perfil: str = f"{nombre_direccion_ranking}/ver_perfil"

    bp_ranking.register_blueprint(perfil_usuario_blueprint(db))

    ranking_service: Ranking = Ranking.getMyRanking(db)

    @bp_ranking.route(f"/{nombre_direccion_ranking}", methods=['GET'])
    def ranking() -> str:
        return render_template("ranking.html", usuarios = ranking_service.mostrarUsuarios())

    return bp_ranking