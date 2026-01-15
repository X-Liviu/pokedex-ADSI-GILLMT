from flask import Blueprint, request, redirect, render_template, url_for, flash
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex


def ver_lista_usuarios_blueprint(db: Connection) -> Blueprint:
    bp_verlistaus = Blueprint("ver_lista_usuarios", __name__)

    @bp_verlistaus.route("/ver_lista_usuarios")
    def ver_lista_usuarios():
        modelo = MarcoDex.getMyMarcoDex(db)
        lista_usuarios = modelo.pedirUsuariosParaAdmin()
        return render_template('ver_lista_usuarios.html', usuarios=lista_usuarios)

    @bp_verlistaus.route("/aprobar_usuario/<string:pNomUsuario>", methods=['POST'])
    def aprobar_usuario(pNomUsuario: str):
        mDex = MarcoDex.getMyMarcoDex(db)
        exito = mDex.procesarAprobadoUsuario(pNomUsuario)
        if exito:
            flash(f"Aprobado: {pNomUsuario}", "success")
        else:
            flash(f"Error al aprobar: {pNomUsuario}", "error")
        return redirect(url_for('ver_lista_usuarios.ver_lista_usuarios'))

    @bp_verlistaus.route("/borrar_usuario/<string:pNomUsuario>", methods=['POST'])
    def borrar_usuario(pNomUsuario: str):
        mDex = MarcoDex.getMyMarcoDex(db)
        mDex.procesarBorradoUsuario(pNomUsuario)
        flash(f"Eliminado: {pNomUsuario}", "info")
        return redirect(url_for('ver_lista_usuarios.ver_lista_usuarios'))

    # --- RUTAS DE MODIFICACIÓN ---

    # 1. GET: Mostrar formulario
    @bp_verlistaus.route("/formulario_modificar_admin/<string:pNomUsuario>", methods=['GET'])
    def formulario_modificar_admin(pNomUsuario: str):
        return render_template('modificar_datos_admin.html', nombre_usuario_vista=pNomUsuario)

    # 2. POST: Procesar formulario
    @bp_verlistaus.route("/procesar_modificacion_admin", methods=['POST'])
    def procesar_modificacion_admin():
        pNomUsuario = request.form.get('usuario_original_hidden')
        pNom = request.form.get('nombre')
        pAp = request.form.get('apellido')
        pNomUsuarioModif = request.form.get('nombre_usuario')

        mDex = MarcoDex.getMyMarcoDex(db)
        exito = mDex.procesarModificarDatosAdmin(pNomUsuario, pNom, pAp, pNomUsuarioModif)
        if exito:
            return redirect(url_for('menu_principal.mostrar_menu'))
        return redirect(url_for('ver_lista_usuarios.ver_lista_usuarios'))

    return bp_verlistaus