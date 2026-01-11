from flask import Blueprint, request, redirect, render_template, flash, url_for, session # <--- Asegúrate de importar session
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex

def identificacion_blueprint(db: Connection) -> Blueprint:
    bp_identificacion = Blueprint("identificacion", __name__)

    @bp_identificacion.route("/identificacion", methods=['GET', 'POST'])
    def identificacion():
        # --- NUEVO: Si ya hay usuario en sesión, echarlo fuera del login ---
        if 'usuario' in session:
            return redirect(url_for('index'))
        # ------------------------------------------------------------------

        if request.method == 'POST':
            usuario_input = request.form['usuario']
            contrasena_input = request.form['contrasena']

            mi_marcodex = MarcoDex.getMyMarcoDex(db)
            exito = mi_marcodex.iniciarSesion(usuario_input, contrasena_input)

            if exito:
                session['usuario'] = usuario_input # Guardamos la sesión aquí
                return redirect(url_for('index'))
            else:
                flash("Usuario o contraseña incorrectos")
                return render_template('pantalla_inicial.html')

        return render_template('pantalla_inicial.html')

    @bp_identificacion.route("/logout")
    def logout():
        # 1. Elimina al usuario de la sesión
        session.clear()
        # 2. Mensaje opcional (si quieres mostrarlo en el login)
        flash("Has cerrado sesión correctamente.")
        # 3. Redirige al login (que ahora se llama 'identificacion')
        return redirect(url_for('identificacion.identificacion'))

    return bp_identificacion