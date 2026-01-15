from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.controller.model.marcoDex_controller import MarcoDex
from app.database.connection import Connection


def confirmar_contrasena_blueprint(db: Connection) -> Blueprint:
    bp = Blueprint("confirmar", __name__)
    mDex = MarcoDex.getMyMarcoDex(db)

    @bp.route("/confirmar_cambios", methods=["GET", "POST"])
    def confirmar_cambios():
        pNomUsuario = session.get('usuario')
        if not pNomUsuario:
            # Si no hay usuario en sesión, volvemos al inicio o login
            return redirect(url_for('modificar_datos.modificar_datos'))

        if request.method == "POST":
            pContrasena = request.form.get("password_actual")

            # LLAMADA ACTUALIZADA:
            # Ahora mDex.confirmarConContraseña devuelve un str (el nombre definitivo) o None.
            nombre_usuario_actualizado = mDex.confirmarConContraseña(pNomUsuario, pContrasena)

            if nombre_usuario_actualizado is not None:
                # ÉXITO:
                # 1. Ya no hace falta llamar a .getNomUsuario(), porque YA ES el string.
                # 2. Actualizamos la session directamente.
                session['usuario'] = nombre_usuario_actualizado

                flash("Datos modificados correctamente.")
                return redirect(url_for('menu_principal.mostrar_menu'))
            else:
                # FALLO (Contraseña incorrecta o error interno)
                flash("Contraseña incorrecta o error al procesar.")

        return render_template('confirmar_contrasena.html')

    return bp