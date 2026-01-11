from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex
import json


def chatbot_blueprint(db):
    nombre_bp = "chatbot"
    bp_chatbot = Blueprint(nombre_bp, __name__)
    mDex = MarcoDex.getMyMarcoDex(db)

    # Función robusta para manejar strings de json.dumps o diccionarios
    def formatear_json_a_html(datos):
        if not datos:
            return "No se encontraron datos."

        # Intentar convertir string (de json.dumps) a diccionario
        if isinstance(datos, str):
            try:
                datos = json.loads(datos)
            except Exception:
                # Si falla la conversión, devolvemos el string tal cual
                return datos

        # Si es un diccionario, lo formateamos con viñetas
        if isinstance(datos, dict):
            html = "<b>Datos obtenidos:</b><br>"
            for clave, valor in datos.items():
                # Reemplazamos guiones bajos por espacios para que se vea mejor
                etiqueta = clave.replace('_', ' ').capitalize()
                html += f"• <b>{etiqueta}:</b> {valor}<br>"
            return html

        return str(datos)

    @bp_chatbot.route('/interfaz', methods=['GET', 'POST'])
    def chatbot_view():

        # 1. PRECARGA: Solo ocurre la primera vez
        if 'menu_json' not in session:
            # Aquí asumimos que precargar_opciones_menu() también podría devolver un string JSON
            res_precarga = mDex.mostrarOpciones()

            # Convertir a dict si es string para poder manipularlo en Python
            if isinstance(res_precarga, str):
                res_precarga = json.loads(res_precarga)

            session['menu_json'] = res_precarga

            opciones = res_precarga.get('opciones', [])
            menu_texto = "<b>Selecciona una opción introduciendo el número:</b><br>"
            menu_texto += "<br>".join(opciones)

            session['historial'] = [{"role": "bot", "content": menu_texto}]
            session['estado'] = "MENU"
            session['opcion_activa'] = None

        if request.method == 'POST':
            user_input = request.form.get('mensaje', '').strip()
            if not user_input:
                return redirect(url_for('chatbot.chatbot_view'))

            temp_historial = session['historial']
            temp_historial.append({"role": "user", "content": user_input})

            if session['estado'] == "MENU":
                if user_input == "5":
                    session.clear()
                    return redirect(url_for('index'))

                elif user_input in ["1", "2", "3", "4"]:
                    session['opcion_activa'] = user_input
                    session['estado'] = "PARAMETRO"

                    prompts = {
                        "1": "Introduce el <b>ID del equipo</b>:",
                        "2": "Introduce el <b>nombre del Pokémon</b> (Fortalezas):",
                        "3": "Introduce el <b>nombre del Pokémon</b> (Evolución):",
                        "4": "Introduce el <b>nombre del Pokémon</b> (Stats):"
                    }
                    temp_historial.append({"role": "bot", "content": prompts.get(user_input)})
                else:
                    temp_historial.append({"role": "bot", "content": "Opción no válida. Introduce 1-5."})

            elif session['estado'] == "PARAMETRO":
                opcion = session['opcion_activa']

                # Llamadas a métodos (que devuelven strings vía json.dumps)
                if opcion == "1":
                    res_raw = mDex.mejorPokemon(user_input)
                elif opcion == "2":
                    res_raw = mDex.obtenerEfectos(user_input)
                elif opcion == "3":
                    res_raw = mDex.cadenaEvolutiva(user_input)
                elif opcion == "4":
                    res_raw = mDex.caracteristicasPokemon(user_input)

                # Pasamos el string JSON a la función de formateo
                resultado_html = formatear_json_a_html(res_raw)
                temp_historial.append({"role": "bot", "content": resultado_html, "separador": True})

                # Reutilizar menú guardado
                opciones_guardadas = session['menu_json'].get('opciones', [])
                menu_reinicio = "<b>Selecciona una opción:</b><br>" + "<br>".join(opciones_guardadas)
                temp_historial.append({"role": "bot", "content": menu_reinicio})

                session['estado'] = "MENU"
                session['opcion_activa'] = None

            session['historial'] = temp_historial
            session.modified = True
            return redirect(url_for('chatbot.chatbot_view'))

        return render_template('chatbot.html', historial=session['historial'])

    return bp_chatbot