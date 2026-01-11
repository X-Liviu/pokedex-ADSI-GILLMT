from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex
import json


def chatbot_blueprint(db: Connection) -> Blueprint:
    nombre_bp = "chatbot"
    bp_chatbot = Blueprint(nombre_bp, __name__)
    mDex = MarcoDex.getMyMarcoDex(db)

    # Función auxiliar para convertir cualquier JSON en texto legible para el chat
    def formatear_json_a_html(datos_json):
        if not datos_json:
            return "No se encontraron datos."

        html = "<b>Datos encontrados:</b><br>"
        for clave, valor in datos_json.items():
            # Formateamos la clave (poniendo la primera letra en mayúscula) y el valor
            html += f"• <b>{clave.capitalize()}:</b> {valor}<br>"
        return html

    @bp_chatbot.route('/chatbot', methods=['GET', 'POST'])
    def chatbot_view():
        # 1. PRECARGA ÚNICA: Guardamos el JSON en la sesión para reutilizarlo
        if 'menu_json' not in session:
            # Solo llamamos a la base de datos la primera vez
            res_json_precarga = mDex.mostrarOpciones()
            session['menu_json'] = res_json_precarga  # Guardamos el JSON entero

            opciones = res_json_precarga.get('opciones', [])
            menu_texto = "<b>Para elegir introduce un número:</b><br>"
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

            # --- ESTADO MENÚ ---
            if session['estado'] == "MENU":
                if user_input == "5":
                    session.clear()  # Borra todo (incluyendo el menu_json) para reiniciar
                    return redirect(url_for('index'))

                elif user_input in ["1", "2", "3", "4"]:
                    session['opcion_activa'] = user_input
                    session['estado'] = "PARAMETRO"

                    prompts = {
                        "1": "Introduce el <b>ID del equipo</b>:",
                        "2": "Introduce el <b>nombre del Pokémon</b> (Características):",
                        "3": "Introduce el <b>nombre del Pokémon</b> (Evolución):",
                        "4": "Introduce el <b>nombre del Pokémon</b> (Stats):"
                    }
                    temp_historial.append({"role": "bot", "content": prompts.get(user_input)})
                else:
                    temp_historial.append({"role": "bot", "content": "Opción no válida. Introduce 1-5."})

            # --- ESTADO PARÁMETRO ---
            elif session['estado'] == "PARAMETRO":
                opcion = session['opcion_activa']

                # Llamadas a métodos independientes
                if opcion == "1":
                    res = mDex.mejorPokemon(user_input)
                elif opcion == "2":
                    res = mDex.obtenerEfectos(user_input)
                elif opcion == "3":
                    res = mDex.cadenaEvolutiva(user_input)
                elif opcion == "4":
                    res = mDex.caracteristicasPokemon(user_input)

                # Convertimos el JSON a una cadena HTML legible
                resultado_formateado = formatear_json_a_html(res)

                # Guardamos en el historial
                temp_historial.append({"role": "bot", "content": resultado_formateado, "separador": True})

                # Reutilizamos el menú guardado anteriormente
                opciones_guardadas = session['menu_json'].get('opciones', [])
                menu_reinicio = "<b>Para elegir introduce un número:</b><br>" + "<br>".join(opciones_guardadas)
                temp_historial.append({"role": "bot", "content": menu_reinicio})

                session['estado'] = "MENU"
                session['opcion_activa'] = None

            session['historial'] = temp_historial
            session.modified = True
            return redirect(url_for('chatbot.chatbot_view'))

        return render_template('chatbot.html', historial=session['historial'])

    return bp_chatbot