from flask import Blueprint, request, redirect, render_template, flash, url_for, session
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex


def registrarse_blueprint(db: Connection) -> Blueprint:
    bp_registrarse = Blueprint("registrarse", __name__)

    @bp_registrarse.route("/registrarse", methods=['GET', 'POST'])
    def registrarse():
        # --- ZONA POST (Procesar formulario) ---
        if request.method == 'POST':
            # 1. Recoger datos
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            correo = request.form['correo']
            usuario = request.form['usuario']
            contrasena = request.form['contrasena']
            contrasena_rep = request.form['contrasena_rep']

            # 2. Llamada al sistema
            mi_marcodex = MarcoDex.getMyMarcoDex(db)
            resultado = mi_marcodex.procesarRegistro(nombre, apellido, correo, usuario, contrasena, contrasena_rep)

            # 3. Evaluar resultado
            if resultado == -1:
                flash("Error: Las contraseñas no coinciden.")
                # Asegúrate de que el nombre del HTML coincida con tu archivo real
                return render_template('registro.html')

            elif resultado == -2:
                flash("Error: El nombre de usuario o el correo ya están en uso.")
                return render_template('registro.html')

            elif resultado == 0:
                # --- ÉXITO: VERIFICACIÓN ROBUSTA ---
                # Intentamos iniciar sesión REALMENTE para asegurar que la BD está bien
                if mi_marcodex.iniciarSesion(usuario, contrasena):
                    # Ahora sí, guardamos la sesión
                    session['usuario'] = usuario

                    rol_real = mi_marcodex.getRol(usuario)
                    session['rol'] = rol_real

                    # Redirección final
                    return redirect(url_for('index'))

                else:
                    # Fallo de seguridad/BD tras el registro
                    flash("Error crítico: El usuario se creó pero no se pudo iniciar sesión.")
                    return render_template('registro.html')

        return render_template('registro.html')

    return bp_registrarse