import json
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.controller.model.marcoDex_controller import MarcoDex
from app.database.connection import Connection

def modificar_equipo_blueprint(db: Connection) -> Blueprint:
    nombre_direccion_crear_equipo: str = "modificar_equipo"
    bp_modificar_equipo = Blueprint(nombre_direccion_crear_equipo, __name__)

    # Obtenemos la instancia única de MarcoDex
    mDex = MarcoDex.getMyMarcoDex(db)

    @bp_modificar_equipo.route("/modificar-equipo/<int:num_equipo>", methods=["GET", "POST"])
    def modificar_equipo(num_equipo):
        nombre_sesion = session.get('username')
        if not nombre_sesion:
            return redirect(url_for('iniciar_sesion'))

        # A. Carga inicial
        if request.method == "GET":
            # Clonamos el equipo original para trabajar sobre una copia
            mDex.clonarEquipo(num_equipo, nombre_sesion)
            session['equipo_en_edicion'] = num_equipo

        # Usamos el num_equipo de la URL, es más fiable que la sesión en el POST
        num_equipo_activo = num_equipo

        # B. Interacción
        if request.method == "POST":
            accion = request.form.get("accion")

            if accion == "aniadir":
                especie = request.form.get("especie")
                nombre_custom = request.form.get("nombre_custom")
                # El modelo añade el bicho a la COPIA del equipo
                mDex.aniadirPokemon(especie, nombre_custom, num_equipo_activo, nombre_sesion)

            elif accion == "borrar":
                pokemon_id = request.form.get("pokemon_id")
                mDex.borrarPokemon(num_equipo_activo, pokemon_id, nombre_sesion)

            elif accion == "guardar":
                # Guardamos los cambios de la copia en la BD y en el objeto real
                mDex.compararCopias(num_equipo_activo, nombre_sesion)
                session.pop('equipo_en_edicion', None)
                return redirect(url_for('ver_equipos.ver_equipos'))

            elif accion == "cancelar":
                # Descartamos la copia y no tocamos la BD
                mDex.descartarCambios(num_equipo_activo, nombre_sesion)
                session.pop('equipo_en_edicion', None)
                # Redirigimos a detalles porque el equipo sigue existiendo tal cual estaba
                return redirect(url_for('ver_detalles.detalles', num=num_equipo_activo))

        # C. Renderizado
        especies_json = mDex.mostrarPokedex()
        # mostrarInfoEquipo debe estar preparado para devolver la INFO DE LA COPIA si existe
        equipo_datos = mDex.mostrarInfoEquipo(num_equipo_activo, nombre_sesion)

        return render_template("modificar_equipo.html",
                               especies=json.loads(especies_json),
                               equipo=equipo_datos,
                               num_equipo=num_equipo_activo)

    return bp_modificar_equipo