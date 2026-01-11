from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.controller.model.marcoDex_controller import MarcoDex
from app.database.connection import Connection


def confirmar_contrasena_blueprint(db: Connection) -> Blueprint:
    bp = Blueprint("confirmar", __name__)
    mDex = MarcoDex.getMyMarcoDex(db)

    @bp.route("/confirmar-cambios", methods=["GET", "POST"])
    def confirmar_cambios():
        pNomUsuario = session.get('usuario')
        if not pNomUsuario:
            return redirect(url_for('modificar_datos.modificar_datos'))

        if request.method == "POST":
            pContrasena = request.form.get("password_actual")

            usuario_obj = mDex.confirmarConContraseña(pNomUsuario, pContrasena)

            if usuario_obj:  # Si no es None, es que funcionó

                # --- AQUÍ ESTÁ LA SOLUCIÓN ---
                # Actualizamos la sesión con el nombre REAL que tiene ahora el usuario
                session['usuario'] = usuario_obj.getNomUsuario() #TODO que se devuelva el Usuario entero a la UI y que acceda ella directamente al atributo del usuario.

                return redirect(url_for('index'))
            else:
                flash("Contraseña incorrecta o error al procesar.")

        return render_template('confirmar_contrasena.html')

    return bp