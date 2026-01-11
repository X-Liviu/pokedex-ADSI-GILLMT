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
            pNomUsuario = request.form['usuario']
            pContrasena = request.form['contrasena']

            mi_marcodex = MarcoDex.getMyMarcoDex(db)
            exito = mi_marcodex.iniciarSesion(pNomUsuario, pContrasena)

            if exito:
                session['usuario'] = pNomUsuario

                # --- IMPORTANTE: Guardamos el rol en sesión ---
                # Esto es lo que usa tu HTML para mostrar u ocultar el botón de Admin
                rol_usuario = mi_marcodex.getRol(pNomUsuario)
                session['rol'] = rol_usuario

                # --- REDIRECCIÓN UNIFICADA ---
                # Tanto Admins como Usuarios van al mismo sitio.
                return redirect(url_for('index'))

            else:
                flash("Usuario o contraseña incorrectos")
                return render_template('pantalla_inicial.html')

        return render_template('pantalla_inicial.html')

    @bp_identificacion.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for('identificacion.identificacion'))

    return bp_identificacion