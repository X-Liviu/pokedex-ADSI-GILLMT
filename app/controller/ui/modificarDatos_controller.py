from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.controller.model.marcoDex_controller import MarcoDex
from app.database.connection import Connection


def modificar_datos_blueprint(db: Connection) -> Blueprint:
    bp = Blueprint("modificar_datos", __name__)
    mDex = MarcoDex.getMyMarcoDex(db)

    @bp.route("/modificar_datos", methods=["GET", "POST"])
    def modificar_datos():
        usuario_actual = session.get('usuario')
        if not usuario_actual:
            return redirect(url_for('identificacion.identificacion'))

        if request.method == "POST":
            # Recoger datos
            pNom = request.form.get("nombre")
            pAp = request.form.get("apellido")
            pCorreo = request.form.get("correo")
            pUsuarioNuevo = request.form.get("usuario")
            pNuevaContra = request.form.get("contrasena")

            # LLAMADA A MARCODEX
            resultado = mDex.procesarSolicitudModificar(usuario_actual, pNom, pAp, pCorreo, pUsuarioNuevo, pNuevaContra)

            # --- NUEVA LÓGICA DE MANEJO DE ERRORES ---
            if resultado == -1:
                # Caso: Sesión corrupta (Usuario no existe)
                session.clear()
                flash("Error de sesión: Usuario no encontrado. Por favor, identifícate de nuevo.")
                return redirect(url_for('identificacion.identificacion'))
            # ----------------------------------------

            elif resultado == 1:
                return redirect(url_for('confirmar.confirmar_cambios'))

            elif resultado == 0:
                # (Tu lógica de éxito directo que corregimos antes)
                if pUsuarioNuevo and pUsuarioNuevo.strip() and pUsuarioNuevo != usuario_actual:
                    session['usuario'] = pUsuarioNuevo
                flash("Datos actualizados correctamente.")
                return redirect(url_for('index'))

        return render_template('modificar_datos.html')

    return bp