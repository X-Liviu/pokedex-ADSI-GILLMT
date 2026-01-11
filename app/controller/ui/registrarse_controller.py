from flask import Blueprint, request, redirect, render_template, flash, url_for, session
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex


def registrarse_blueprint(db: Connection) -> Blueprint:
    bp_registrarse = Blueprint("registrarse", __name__)

    @bp_registrarse.route("/registrarse", methods=['GET', 'POST'])
    def registrarse():
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
                return render_template('registro.html')

            elif resultado == -2:
                flash("Error: El nombre de usuario o el correo ya están en uso.")
                return render_template('registro.html')

            elif resultado == 0:
                # --- ÉXITO: AUTO-LOGIN ---
                session['usuario'] = usuario

                rol_real = mi_marcodex.getRol(usuario)
                session['rol'] = rol_real

                if rol_real == 'NOVERIF':
                    flash(f"Registro completado. ¡Vaya! Has tenido mala suerte y tu rol es {rol_real}.")
                else:
                    flash(f"Registro completado. ¡Bienvenido Entrenador Verificado!")

                return redirect(url_for('index'))  # Nos lleva al menú principal directamente

        return render_template('registro.html')

    return bp_registrarse