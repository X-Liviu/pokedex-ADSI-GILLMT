from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex


def ver_amigos_blueprint(db: Connection):
    bp_amigos = Blueprint("amigos", __name__)

    # RUTA 1: VER LISTA (Sin cambios mayores, solo asegurando lógica existente)
    @bp_amigos.route("/ver_amigos")
    def ver_amigos():
        usuario_actual = session.get('usuario')
        if not usuario_actual:
            return redirect(url_for('login.login'))

        # NOTA: Para ver la lista completa (borrar amigo), necesitarías implementar
        # un método 'obtenerListaAmigos' o similar en MarcoDex/GestorUsuario
        # que rellene la lista memoria desde BD si está vacía.
        # Por ahora lo dejamos como estaba en tu código original.
        marco = MarcoDex.getMyMarcoDex(db)
        # Asumimos que tienes un método para obtener lista (no pedido en este prompt)
        # lista_amigos = marco.obtenerListaAmigos(usuario_actual)
        lista_amigos = []
        return render_template('ver_amigos.html', amigos=lista_amigos)

    # RUTA 2: AÑADIR AMIGO (ACTUALIZADA)
    @bp_amigos.route("/aniadir_amigo", methods=['GET', 'POST'])
    def aniadir_amigo():
        pNomUsuario = session.get('usuario')
        if not pNomUsuario:
            return redirect(url_for('login.login'))

        mDex = MarcoDex.getMyMarcoDex(db)
        usuarios_encontrados = []
        query = request.args.get('q')

        if not query and request.method == 'POST' and 'buscador' in request.form:
            query = request.form['buscador']

        # 1. BÚSQUEDA
        if query:
            usuarios_encontrados = mDex.buscarUsuariosConFiltro(pNomUsuario, query)

        # 2. AÑADIR (POST del botón añadir)
        if request.method == 'POST' and 'nombre_usuario_seleccionado' in request.form:
            pNomUsuarioAmigo = request.form['nombre_usuario_seleccionado']
            if pNomUsuarioAmigo:
                exito = mDex.aniadirAmigo(pNomUsuario, pNomUsuarioAmigo)
                if exito:
                    flash(f"¡{pNomUsuarioAmigo} añadido a tus amigos!", "success")
                    # Refrescamos la búsqueda para que desaparezca de la lista o cambie estado
                    if query:
                        usuarios_encontrados = mDex.buscarUsuariosConFiltro(pNomUsuario, query)
                else:
                    flash(f"No se pudo añadir a {pNomUsuarioAmigo}.", "error")

        return render_template('aniadir_amigo.html', usuarios=usuarios_encontrados, busqueda=query)

    # RUTA 3: BORRAR AMIGO (Sin cambios por ahora)
    @bp_amigos.route("/borrar_amigo", methods=['POST'])
    def borrar_amigo():
        # ... (Tu implementación de borrado) ...
        return redirect(url_for('amigos.ver_amigos'))

    return bp_amigos