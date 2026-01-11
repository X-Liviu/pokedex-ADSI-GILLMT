from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.controller.model.marcoDex_controller import MarcoDex
from app.database.connection import Connection


def modificar_datos_blueprint(db: Connection) -> Blueprint:
    bp = Blueprint("modificar_datos", __name__)
    mDex = MarcoDex.getMyMarcoDex(db)

    @bp.route("/modificar_datos", methods=["GET", "POST"])
    def modificar_datos():
        pNomUsuario = session.get('usuario')
        if not pNomUsuario:
            return redirect(url_for('identificacion.identificacion'))

        if request.method == "POST":
            pNom = request.form.get("nombre")
            pAp = request.form.get("apellido")
            pCorreo = request.form.get("correo")
            pUsuarioNuevo = request.form.get("usuario")
            pNuevaContra = request.form.get("contrasena")

            resultado = mDex.procesarSolicitudModificar(pNomUsuario, pNom, pAp, pCorreo, pUsuarioNuevo, pNuevaContra)

            if resultado == -1:
                session.clear()
                flash("Error de sesión: Usuario no encontrado. Por favor, identifícate de nuevo.")
                return redirect(url_for('identificacion.identificacion'))

            elif resultado == 1:
                return redirect(url_for('confirmar.confirmar_cambios'))

            elif resultado == 0:
                if pUsuarioNuevo and pUsuarioNuevo.strip() and pUsuarioNuevo != pNomUsuario:
                    session['usuario'] = pUsuarioNuevo
                return redirect(url_for('index'))

        return render_template('modificar_datos.html')

    return bp