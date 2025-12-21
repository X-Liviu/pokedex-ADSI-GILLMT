from flask import Blueprint, request, redirect, render_template, flash

from app.controller.model.book_controller import BookController
from app.database.connection import Connection

def ranking_blueprint(db: Connection) -> Blueprint:
    nombre_direccion: str = "ranking"
    bp = Blueprint(nombre_direccion, __name__)

    @bp.route(f"/{nombre_direccion}", methods=['GET'])
    def ranking() -> str:
        return render_template("ranking.html")

    return bp