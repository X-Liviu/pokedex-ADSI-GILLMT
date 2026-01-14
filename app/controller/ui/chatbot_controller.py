from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex
import json


def chatbot_blueprint(db):
    nombre_bp = "chatbot"
    bp_chatbot = Blueprint(nombre_bp, __name__)

    from app.controller.model.marcoDex_controller import MarcoDex
    mDex = MarcoDex.getMyMarcoDex(db)

    def dict_a_html(datos):
        if not datos:
            return "No se encontraron datos."
        if isinstance(datos, str):
            return datos

        html = "<b>Datos obtenidos:</b><br>"
        # Si el resultado de los otros métodos también fuera una lista
        if isinstance(datos, list):
            for item in datos:
                html += f"• {item}<br>"
        else:
            for clave, valor in datos.items():
                etiqueta = clave.replace('_', ' ').capitalize()
                html += f"• <b>{etiqueta}:</b> {valor}<br>"
        return html

    @bp_chatbot.route('/interfaz', methods=['GET', 'POST'])
    def chatbot_view():
        # 1. PRECARGA: Manejando lista de diccionarios
        if 'menu_texto' not in session:
            # res_lista_dicts es algo como: [{"opcion": "1-Ver..."}, {"opcion": "2-Ver..."}]
            res_lista_dicts = mDex.mostrarOpciones()

            # Extraemos solo el texto de cada diccionario para formar el menú
            opciones_texto = [d.get('Opción') for d in res_lista_dicts]

            menu_texto = "<b>Para elegir introduce un número:</b><br>"
            menu_texto += "<br>".join(opciones_texto)

            session['menu_texto'] = menu_texto  # Guardamos el texto ya montado
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
                        "1": "Introduce ID equipo:",
                        "2": "Introduce Pokémon (Fortalezas):",
                        "3": "Introduce Pokémon (Evolución):",
                        "4": "Introduce Pokémon (Stats):"
                    }
                    temp_historial.append({"role": "bot", "content": prompts.get(user_input)})
                else:
                    temp_historial.append({"role": "bot", "content": "Opción no válida (1-5)."})

            elif session['estado'] == "PARAMETRO":
                opcion = session['opcion_activa']
                res_data = None

                if opcion == "1":
                    res_data = mDex.mejorPokemon(user_input)
                elif opcion == "2":
                    res_data = mDex.obtenerEfectos(user_input)
                elif opcion == "3":
                    res_data = mDex.cadenaEvolutiva(user_input)
                elif opcion == "4":
                    res_data = mDex.caracteristicasPokemon(user_input)

                resultado_formateado = dict_a_html(res_data)
                temp_historial.append({"role": "bot", "content": resultado_formateado, "separador": True})

                # REUTILIZACIÓN: Usamos el texto del menú guardado en sesión
                temp_historial.append({"role": "bot", "content": session['menu_texto']})

                session['estado'] = "MENU"
                session['opcion_activa'] = None

            session['historial'] = temp_historial
            session.modified = True
            return redirect(url_for('chatbot.chatbot_view'))

        return render_template('chatbot.html', historial=session['historial'])

    return bp_chatbot