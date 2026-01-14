from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from app.database.connection import Connection
from app.controller.model.marcoDex_controller import MarcoDex
import json


def chatbot_blueprint(db):
    nombre_bp = "chatbot"
    bp_chatbot = Blueprint(nombre_bp, __name__)

    from app.controller.model.marcoDex_controller import MarcoDex
    mDex = MarcoDex.getMyMarcoDex(db)

    # Función para convertir el dict de datos a HTML
    def dict_a_html(datos):
        # Si llegamos aquí y es un dict vacío o algo inesperado
        if not datos or not isinstance(datos, dict):
            return "No se ha podido procesar la información."

        html = "<b>Información encontrada:</b><br>"
        for clave, valor in datos.items():
            etiqueta = clave.replace('_', ' ').capitalize()
            html += f"• <b>{etiqueta}:</b> {valor}<br>"
        return html

    @bp_chatbot.route('/interfaz', methods=['GET', 'POST'])
    def chatbot_view():
        # --- PRECARGA DEL MENÚ ---
        if 'menu_texto' not in session:
            res_lista_dicts = mDex.mostrarOpciones()
            opciones_texto = [f"{d.get('Opción')} - {d.get('Descripción')}" for d in res_lista_dicts]

            menu_texto = "<b>Para elegir introduce un número:</b><br>"
            menu_texto += "<br>".join(opciones_texto)

            session['menu_texto'] = menu_texto
            session['historial'] = [{"role": "bot", "content": menu_texto}]
            session['estado'] = "MENU"
            session['opcion_activa'] = None

        if request.method == 'POST':
            user_input = request.form.get('mensaje', '').strip()
            if not user_input:
                return redirect(url_for('chatbot.chatbot_view'))

            temp_historial = session['historial']
            temp_historial.append({"role": "user", "content": user_input})

            # --- ESTADO 1: MENÚ ---
            if session['estado'] == "MENU":
                if user_input == "5":
                    session.pop('historial', None)
                    session.pop('menu_texto', None)
                    session.pop('estado', None)
                    return redirect(url_for('index'))

                elif user_input in ["1", "2", "3", "4"]:
                    session['opcion_activa'] = user_input
                    session['estado'] = "PARAMETRO"

                    prompts = {
                        "1": "Introduce el <b>ID del equipo</b>:",
                        "2": "Introduce el nombre del Pokémon (Fortalezas):",
                        "3": "Introduce el nombre (Evolución):",
                        "4": "Introduce el nombre (Stats):"
                    }
                    temp_historial.append({"role": "bot", "content": prompts.get(user_input)})
                else:
                    temp_historial.append(
                        {"role": "bot", "content": "Opción no válida. Introduce un número del 1 al 5."})

            # --- ESTADO 2: PROCESAR PARÁMETRO ---
            elif session['estado'] == "PARAMETRO":
                opcion = session['opcion_activa']
                res_data = None

                # Llamada a los métodos
                if opcion == "1":
                    usuario = session.get('usuario', 'Invitado')
                    res_data = mDex.mejorPokemon(usuario, user_input)
                elif opcion == "2":
                    res_data = mDex.obtenerEfectos(user_input)
                elif opcion == "3":
                    res_data = mDex.cadenaEvolutiva(user_input)
                elif opcion == "4":
                    res_data = mDex.caracteristicasPokemon(user_input)

                # --- VALIDACIÓN DEL ERROR -1 ---
                if res_data == -1:
                    mensaje_error = "⚠️ <b>Error:</b> No se han encontrado resultados para tu búsqueda con. Por favor, inténtalo de nuevo."
                    temp_historial.append({"role": "bot", "content": mensaje_error, "separador": True})
                else:
                    # Si no es -1, es un diccionario, así que lo formateamos
                    resultado_formateado = dict_a_html(res_data)
                    temp_historial.append({"role": "bot", "content": resultado_formateado, "separador": True})

                # En ambos casos (éxito o error), volvemos a mostrar el menú
                temp_historial.append({"role": "bot", "content": session['menu_texto']})

                session['estado'] = "MENU"
                session['opcion_activa'] = None

            session['historial'] = temp_historial
            session.modified = True
            return redirect(url_for('chatbot.chatbot_view'))

        return render_template('chatbot.html', historial=session['historial'])

    return bp_chatbot