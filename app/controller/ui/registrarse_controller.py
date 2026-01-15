from flask import Blueprint, request, redirect, render_template, flash, url_for, session
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex

def registrarse_blueprint(db: Connection) -> Blueprint:
    bp_registrarse = Blueprint("registrarse", __name__)

    @bp_registrarse.route("/registrarse", methods=['GET', 'POST'])
    def registrarse():
        if request.method == 'POST':
            # 1. Recoger datos
            pNom = request.form.get('nombre', '')
            pAp = request.form.get('apellido', '')
            pCorreo = request.form.get('correo', '')
            pNomUsuario = request.form.get('usuario', '')
            pContrasena = request.form.get('contrasena', '')
            pContrasenaRep = request.form.get('contrasena_rep', '')

            if not pNom or not pAp or not pCorreo or not pNomUsuario or not pContrasena or not pContrasenaRep:
                flash("Error: No es posible con campos vacíos.")
                return render_template('registro.html')

            try:
                # 2. Llamada al sistema (ENVOLVEMOS EN TRY-EXCEPT)
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
                    # ÉXITO
                    if mi_marcodex.iniciarSesion(pNomUsuario, pContrasena):
                        session['usuario'] = pNomUsuario
                        session['rol'] = mi_marcodex.getRol(pNomUsuario)
                        return redirect(url_for('menu_principal.mostrar_menu'))
                    else:
                        flash("Error crítico: Algo falló en el sistema.")
                        return render_template('registro.html')

            except Exception as e:
                print(f"Error técnico en registro: {e}")
                flash("Error crítico: Fallo en el sistema.")
                return render_template('registro.html')

        return render_template('registro.html')

    return bp_registrarse