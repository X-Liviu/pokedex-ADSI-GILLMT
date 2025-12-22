from flask import Blueprint, request, redirect, render_template, flash

from app.controller.model.ranking_controller import Ranking
from app.database.connection import Connection

def ranking_blueprint(db: Connection) -> Blueprint:
    nombre_direccion: str = "ranking"
    bp = Blueprint(nombre_direccion, __name__)

    ranking_service: Ranking = Ranking.getMyRanking()

    if ranking_service == None:
        ranking_service = Ranking(db)

    @bp.route(f"/{nombre_direccion}", methods=['GET'])
    def ranking() -> str:
        return render_template("ranking.html")

    return bp