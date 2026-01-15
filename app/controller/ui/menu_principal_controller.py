from flask import Blueprint, render_template
from app.database.connection import Connection


def menu_principal_blueprint(db: Connection) -> Blueprint:
    menu_principal_bp = Blueprint('menu_principal', __name__)

    @menu_principal_bp.route('/menu', methods=['GET'])
    def mostrar_menu():
        return render_template('menu_principal.html')

    return menu_principal_bp