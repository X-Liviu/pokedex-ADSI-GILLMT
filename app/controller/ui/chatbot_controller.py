from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex
import json


def chatbot_blueprint(db):
    nombre_bp = "chatbot"
    bp_chatbot = Blueprint(nombre_bp, __name__)
    mDex = MarcoDex.getMyMarcoDex(db)

    @bp_chatbot.route('/chatbot', methods=['GET', 'POST'])
    def chatbot_view():
        # 1. PRECARGA: Obtenemos el string JSON inicial
        if 'menu_json' not in session:
            res_json_string = mDex.mostrarOpciones()  # Esto devuelve un string

            # Solo para extraer las opciones una vez, lo cargamos temporalmente
            datos_dict = json.loads(res_json_string)
            session['opciones_menu'] = datos_dict.get('opciones', [])

            menu_texto = "<b>Para elegir introduce un número:</b><br>"
            menu_texto += "<br>".join(session['opciones_menu'])

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
                        "1": "Introduce ID equipo:", "2": "Introduce Pokémon (Fortalezas):",
                        "3": "Introduce Pokémon (Evolución):", "4": "Introduce Pokémon (Stats):"
                    }
                    temp_historial.append({"role": "bot", "content": prompts.get(user_input)})
                else:
                    temp_historial.append({"role": "bot", "content": "Opción no válida (1-5)."})

            elif session['estado'] == "PARAMETRO":
                opcion = session['opcion_activa']

                # Obtenemos el string JSON tal cual (json.dumps)
                if opcion == "1":
                    res_raw = mDex.mejorPokemon(user_input)
                elif opcion == "2":
                    res_raw = mDex.obtenerEfectos(user_input)
                elif opcion == "3":
                    res_raw = mDex.cadenaEvolutiva(user_input)
                elif opcion == "4":
                    res_raw = mDex.caracteristicasPokemon(user_input)

                # Lo metemos en una etiqueta <pre> para que se vea como bloque de código
                resultado_formateado = f"<pre style='background:#f4f4f4; padding:10px; border:1px solid #ccc; border-radius:10px; font-size:14px; overflow-x:auto;'>{res_raw}</pre>"

                temp_historial.append({"role": "bot", "content": resultado_formateado, "separador": True})

                # Reutilizamos el menú
                menu_reinicio = "<b>Para elegir introduce un número:</b><br>" + "<br>".join(session['opciones_menu'])
                temp_historial.append({"role": "bot", "content": menu_reinicio})

                session['estado'] = "MENU"
                session['opcion_activa'] = None

            session['historial'] = temp_historial
            session.modified = True
            return redirect(url_for('chatbot.chatbot_view'))

        return render_template('chatbot.html', historial=session['historial'])

    return bp_chatbot