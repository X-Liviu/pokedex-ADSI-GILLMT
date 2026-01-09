from flask import Blueprint, render_template

# Definimos el Blueprint
menu_principal_bp = Blueprint('menu_principal', __name__)

@menu_principal_bp.route('/menu', methods=['GET'])
def mostrar_menu():
    return render_template('menu_principal.html')