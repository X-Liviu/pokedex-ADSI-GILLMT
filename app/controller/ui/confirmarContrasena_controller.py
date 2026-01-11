from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.controller.model.marcoDex_controller import MarcoDex
from app.database.connection import Connection


def confirmar_contrasena_blueprint(db: Connection) -> Blueprint:
    bp = Blueprint("confirmar", __name__)
    mDex = MarcoDex.getMyMarcoDex(db)

    @bp.route("/confirmar-cambios", methods=["GET", "POST"])
    def confirmar_cambios():
        usuario_actual = session.get('usuario')
        if not usuario_actual:
            return redirect(url_for('modificar_datos.modificar_datos'))

        if request.method == "POST":
            pContrasena = request.form.get("password_actual")

            # LLAMADA A MARCODEX
            # Ahora 'resultado' será el objeto Usuario si salió bien, o None si salió mal
            usuario_obj = mDex.confirmarConContraseña(usuario_actual, pContrasena)

            if usuario_obj:  # Si no es None, es que funcionó

                # --- AQUÍ ESTÁ LA SOLUCIÓN ---
                # Actualizamos la sesión con el nombre REAL que tiene ahora el usuario
                session['usuario'] = usuario_obj.getNomUsuario()

                flash("Perfil actualizado con éxito.")
                return redirect(url_for('index'))
            else:
                flash("Contraseña incorrecta o error al procesar.")

        return render_template('confirmar_contrasena.html')

    return bp