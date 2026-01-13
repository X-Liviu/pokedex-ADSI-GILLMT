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
            return redirect(url_for('identificacion.identificacion'))

        marco = MarcoDex.getMyMarcoDex(db)

        # IMPLEMENTACIÓN: Llamamos al método que devuelve la lista de diccionarios
        lista_amigos = marco.obtenerListaAmigos(usuario_actual)

        return render_template('ver_amigos.html', amigos=lista_amigos)

    # RUTA 2: AÑADIR AMIGO (ACTUALIZADA)
    @bp_amigos.route("/aniadir_amigo", methods=['GET', 'POST'])
    def aniadir_amigo():
        pNomUsuario = session.get('usuario')
        if not pNomUsuario:
            return redirect(url_for('identificacion.identificacion'))

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

    # RUTA 3: BORRAR AMIGO (IMPLEMENTADA)
    @bp_amigos.route("/borrar_amigo", methods=['POST'])
    def borrar_amigo():
        usuario_actual = session.get('usuario')
        if not usuario_actual:
            return redirect(url_for('identificacion.identificacion'))

        # Obtenemos el nombre del amigo desde el formulario oculto en el HTML
        nombre_amigo = request.form.get('nombre_amigo')

        if nombre_amigo:
            marco = MarcoDex.getMyMarcoDex(db)

            # Pasos 4 a 11 del diagrama ocurren aquí dentro
            # Aunque devuelve la lista JSON, al ser una petición web normal,
            # redirigimos a la vista principal para repintar
            marco.procesarBorradoAmigo(nombre_amigo, usuario_actual)

            flash(f"Amigo {nombre_amigo} eliminado.", "success")

        return redirect(url_for('amigos.ver_amigos'))

    return bp_amigos