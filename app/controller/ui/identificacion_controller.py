from flask import Blueprint, request, redirect, render_template, flash, url_for, session
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex


def identificacion_blueprint(db: Connection) -> Blueprint:
    bp_identificacion = Blueprint("identificacion", __name__)

    @bp_identificacion.route("/identificacion", methods=['GET', 'POST'])
    def identificacion():
        # 1. Si ya está logueado, mandamos a TODOS al menú principal (index)
        if 'usuario' in session:
            return redirect(url_for('index'))

        if request.method == 'POST':
            pNomUsuario = request.form.get('usuario')
            pContrasena = request.form.get('contrasena')

            # --- VALIDACIÓN PREVIA ---
            # Verificamos que los datos hayan llegado antes de molestar a la BD
            if not pNomUsuario or not pContrasena:
                flash("Por favor, rellene todos los campos.")
                return render_template('pantalla_inicial.html')

            try:
                # Intentamos conectar y validar
                mi_marcodex = MarcoDex.getMyMarcoDex(db)
                exito = mi_marcodex.iniciarSesion(pNomUsuario, pContrasena)

                if exito:
                    session['usuario'] = pNomUsuario

                    # --- IMPORTANTE: Guardamos el rol en sesión ---
                    rol_usuario = mi_marcodex.getRol(pNomUsuario)
                    session['rol'] = rol_usuario

                    # --- REDIRECCIÓN UNIFICADA ---
                    return redirect(url_for('index'))

                else:
                    flash("Usuario o contraseña incorrectos")
                    return render_template('pantalla_inicial.html')

            except Exception as e:
                # CAPTURA DEL ERROR TÉCNICO
                print(f"Error técnico en login: {e}")
                flash("Error técnico o de conexión.")
                return render_template('pantalla_inicial.html')

        return render_template('pantalla_inicial.html')

    @bp_identificacion.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for('identificacion.identificacion'))

    return bp_identificacion