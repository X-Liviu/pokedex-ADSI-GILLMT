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
            pNom = request.form['nombre']
            pAp = request.form['apellido']
            pCorreo = request.form['correo']
            pNomUsuario = request.form['usuario']
            pContrasena = request.form['contrasena']
            pContrasenaRep = request.form['contrasena_rep']

            # 2. Llamada al sistema
            mi_marcodex = MarcoDex.getMyMarcoDex(db)
            resultado = mi_marcodex.procesarRegistro(pNom, pAp, pCorreo, pNomUsuario, pContrasena, pContrasenaRep)

            # 3. Evaluar resultado
            if resultado == -1:
                flash("Error: Las contraseñas no coinciden.")
                return render_template('registro.html')

            elif resultado == -2:
                flash("Error: El nombre de usuario o el correo ya están en uso.")
                return render_template('registro.html')

            elif resultado == 0:
                # --- ÉXITO: VERIFICACIÓN ROBUSTA ---
                # Intentamos iniciar sesión REALMENTE para asegurar que la BD está bien
                if mi_marcodex.iniciarSesion(pNomUsuario, pContrasena):
                    # Ahora sí, guardamos la sesión
                    session['usuario'] = pNomUsuario

                    rol_real = mi_marcodex.getRol(pNomUsuario)
                    session['rol'] = rol_real

                    # Redirección final
                    return redirect(url_for('index'))

                else:
                    # Fallo de seguridad/BD tras el registro
                    flash("Error crítico: El usuario se creó pero no se pudo iniciar sesión.")
                    return render_template('registro.html')

        return render_template('registro.html')

    return bp_registrarse