import json
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.controller.model.marcoDex_controller import MarcoDex
from app.database.connection import Connection

def crear_equipo_blueprint(db: Connection) -> Blueprint:
    nombre_direccion_crear_equipo: str = "crear_equipo"
    bp_crear_equipo = Blueprint(nombre_direccion_crear_equipo, __name__)

    # Obtenemos la instancia única de MarcoDex
    mDex = MarcoDex.getMyMarcoDex(db)

    @bp_crear_equipo.route("/crear-equipo", methods=["GET", "POST"])
    def crear_equipo():
        nombre_sesion = session.get('username')

        #PRUEBA TATA
        # if not session.get('username'):
        #     session['username'] = 'Tata'

        if not nombre_sesion:
            return redirect(url_for('iniciar_sesion'))

        # A. Si entramos por primera vez (clic en "Crear Nuevo")
        if request.method == "GET":
            # Creamos el equipo vacío en el modelo y guardamos el ID en sesión
            num_nuevo = mDex.newEquipo(nombre_sesion)
            session['equipo_en_edicion'] = num_nuevo

        num_equipo = session.get('equipo_en_edicion')

        # B. Si el usuario interactúa con la pantalla (Añadir, Guardar, Cancelar)
        if request.method == "POST":
            accion = request.form.get("accion")

            if accion == "aniadir":
                especie = request.form.get("especie")
                nombre_custom = request.form.get("nombre_custom")
                # Intentamos añadir (el modelo controla que no pase de 6)
                resultado = mDex.aniadirPokemon(especie, nombre_custom, num_equipo, nombre_sesion)
                if resultado == -1:
                    flash("¡El equipo ya está completo (máximo 6)!")

            elif accion == "guardar":
                # Persistencia final en la Base de Datos
                mDex.guardarEquipo(num_equipo, nombre_sesion)
                session.pop('equipo_en_edicion', None)
                return redirect(url_for('ver_equipos.ver_equipos'))

            elif accion == "cancelar":
                # Eliminamos el equipo de la memoria del usuario
                mDex.borrarEquipo(num_equipo, nombre_sesion)
                session.pop('equipo_en_edicion', None)
                return redirect(url_for('ver_equipos.ver_equipos'))

        # C. Renderizado: Siempre cargamos los datos actualizados para pintar los dos lados
        # Lado izquierdo: Todas las especies disponibles
        especies_json = mDex.mostrarPokedex()
        # Lado derecho: El equipo actual con sus filas rosas
        equipo_datos = mDex.mostrarInfoEquipo(num_equipo, nombre_sesion)

        return render_template("crear_equipo.html",
                               especies=json.loads(especies_json),
                               equipo=equipo_datos,
                               num_equipo=num_equipo)

    return bp_crear_equipo