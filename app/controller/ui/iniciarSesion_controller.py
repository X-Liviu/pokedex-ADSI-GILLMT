from flask import Blueprint, render_template, session, request
from app.controller.model.marcoDex_controller import MarcoDex

bp_iniciar = Blueprint('iniciar_sesion', __name__)

@bp_iniciar.route('/iniciar_sesion')
def iniciar_sesion():
    return render_template('iniciar_sesion.html')

def iniciar_sesion_blueprint(db):
    return bp_iniciar