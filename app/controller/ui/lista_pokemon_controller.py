from flask import Blueprint, request, redirect, render_template, flash
from app.database.connection import Connection
import json
from app.controller.model.marcoDex_controller import MarcoDex


def lista_pokemon_blueprint(db: Connection) -> Blueprint:
    bp_listap = Blueprint("lista_pokemon", __name__)

    @bp_listap.route("/lista_pokemon")
    def lista_pokemon():
        mDex = MarcoDex.getMyMarcoDex(db)

        tipo_filtro = request.args.get('filtro', 'nombre')  # Por defecto 'nombre'
        valor_busqueda = request.args.get('valor')

        if valor_busqueda:
            # Paso 2 del diagrama de filtros: aplicarFiltro(filtro, valor)
            json_recibido = mDex.aplicarFiltro(tipo_filtro, valor_busqueda)
        else:
            json_recibido = mDex.mostrarPokedex()

        # Convertimos el JSON string a lista de Python para el HTML
        lista_pokemon_final = json.loads(json_recibido)

        return render_template('lista_pokemon.html',
                               lista_pokemon=lista_pokemon_final)

    return bp_listap