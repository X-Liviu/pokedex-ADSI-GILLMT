import json
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.controller.model.marcoDex_controller import MarcoDex
from app.database.connection import Connection


def crear_equipo_blueprint(db: Connection) -> Blueprint:
    nombre_direccion_crear_equipo: str = "crear_equipo"
    bp_crear_equipo = Blueprint(nombre_direccion_crear_equipo, __name__)

    mDex = MarcoDex.getMyMarcoDex(db)

    @bp_crear_equipo.route("/crear-equipo", methods=["GET", "POST"])
    def crear_equipo():
        # 1. Identificar al usuario
        # --- CORRECCIÓN 1: Usar 'usuario' (que es como lo guardamos en el login) ---
        nombre_sesion = session.get('usuario')

        if not nombre_sesion:
            # --- CORRECCIÓN 2: Apuntar al blueprint correcto del login ---
            return redirect(url_for('identificacion.identificacion'))

            # 2. CAPTURAR EL ORIGEN
        origen = request.form.get("origen") or request.args.get("origen", "menu")

        # A. Si entramos por primera vez
        if request.method == "GET":
            num_nuevo = mDex.newEquipo(nombre_sesion)
            session['equipo_en_edicion'] = num_nuevo

        num_equipo = session.get('equipo_en_edicion')

        # B. Interacción con la pantalla
        if request.method == "POST":
            accion = request.form.get("accion")

            if accion == "aniadir":
                especie = request.form.get("especie")
                nombre_custom = request.form.get("nombre_custom")
                resultado = mDex.aniadirPokemon(especie, nombre_custom, num_equipo, nombre_sesion)
                if resultado == -1:
                    flash("¡El equipo ya está completo (máximo 6)!")
                elif resultado == -2:
                    flash("Ya tienes un Pokemon que se llama así!!")
                elif resultado == -3:
                    flash("Esta especie ya está en tu equipo")

            elif accion == "borrar":
                pokemon_id = request.form.get("pokemon_id")
                mDex.borrarPokemon(num_equipo, pokemon_id, nombre_sesion)
                flash("Pokémon eliminado del equipo")

            elif accion == "guardar":
                mDex.guardarEquipo(num_equipo, nombre_sesion)
                session.pop('equipo_en_edicion', None)
                flash("¡Equipo creado con éxito!")

                # REDIRECCIÓN DINÁMICA
                if origen == 'mis_equipos':
                    return redirect(url_for('ver_equipos.ver_equipos'))
                # --- CORRECCIÓN 3: Redirigir a 'index' (que es el menú principal) ---
                return redirect(url_for('index'))

            elif accion == "cancelar":
                mDex.borrarEquipo(num_equipo, nombre_sesion)
                session.pop('equipo_en_edicion', None)

                # REDIRECCIÓN DINÁMICA
                if origen == 'mis_equipos':
                    return redirect(url_for('ver_equipos.ver_equipos'))
                # --- CORRECCIÓN 3: Redirigir a 'index' ---
                return redirect(url_for('index'))

        # C. Renderizado
        especies_json = mDex.mostrarPokedex()
        equipo_datos = mDex.mostrarInfoEquipo(num_equipo, nombre_sesion)

        return render_template("crear_equipo.html",
                               especies=json.loads(especies_json),
                               equipo=equipo_datos,
                               num_equipo=num_equipo,
                               origen=origen)

    return bp_crear_equipo