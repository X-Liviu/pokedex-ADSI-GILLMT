from flask import Blueprint, request, redirect, render_template, url_for, flash
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex


def ver_lista_usuarios_blueprint(db: Connection) -> Blueprint:
    bp_verlistaus = Blueprint("ver_lista_usuarios", __name__)

    @bp_verlistaus.route("/ver_lista_usuarios")
    def ver_lista_usuarios():
        # 1. Obtenemos la instancia de la fachada
        modelo = MarcoDex.getMyMarcoDex(db)

        # 2. Pedimos los usuarios (Flujo: pedirUsuariosParaAdmin)
        # Esto devuelve la lista de diccionarios que Jinja necesita
        lista_usuarios = modelo.pedirUsuariosParaAdmin()

        # 3. Renderizamos pasando la lista CORREGIDA
        return render_template('ver_lista_usuarios.html', usuarios=lista_usuarios)

    # ---------------------------------------------------------
    # RUTAS DE ACCIÓN (POST desde el HTML)
    # ---------------------------------------------------------

    @bp_verlistaus.route("/aprobar_usuario/<string:nombre_usuario>", methods=['POST'])
    def aprobar_usuario(nombre_usuario):
        modelo = MarcoDex.getMyMarcoDex(db)
        exito = modelo.procesarAprobadoUsuario(nombre_usuario)

        if exito:
            flash(f"Usuario {nombre_usuario} aprobado correctamente.", "success")
        else:
            flash(f"Error al aprobar a {nombre_usuario}.", "error")

        return redirect(url_for('ver_lista_usuarios.ver_lista_usuarios'))

    @bp_verlistaus.route("/borrar_usuario/<string:nombre_usuario>", methods=['POST'])
    def borrar_usuario(nombre_usuario):
        modelo = MarcoDex.getMyMarcoDex(db)
        # El método devuelve la lista nueva, pero como hacemos redirect,
        # se volverá a pedir en la siguiente petición.
        modelo.procesarBorradoUsuario(nombre_usuario)

        flash(f"Usuario {nombre_usuario} eliminado.", "info")
        return redirect(url_for('ver_lista_usuarios.ver_lista_usuarios'))

    # Esta ruta se llamaría desde la futura pantalla de "Modificar Datos"
    @bp_verlistaus.route("/procesar_modificacion_admin", methods=['POST'])
    def procesar_modificacion_admin():
        # Recoger datos del formulario (Fig. 10)
        usuario_original = request.form.get('usuario_original')
        nuevo_nombre = request.form.get('nombre')
        nuevo_apellido = request.form.get('apellido')
        nuevo_usuario = request.form.get('nombre_usuario')

        modelo = MarcoDex.getMyMarcoDex(db)
        modelo.procesarModificarDatosAdmin(usuario_original, nuevo_nombre, nuevo_apellido, nuevo_usuario)

        flash("Usuario modificado correctamente", "success")
        return redirect(url_for('ver_lista_usuarios.ver_lista_usuarios'))

    return bp_verlistaus