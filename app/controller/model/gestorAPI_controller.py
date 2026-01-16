import pokebase as pb
from typing import List, Dict, Any


class GestorAPI:
    """
    Clase encargada de interactuar con la librería pokebase (API)
    y devolver datos estructurados listos para la BD.
    """

    @staticmethod
    def cargarPokemons() -> List[Dict[str, Any]]:
        lista_datos = []
        print("--- CARGANDO POKÉMON ---")

        # Vamos a cargar del 1 al 15 (Bulbasaur a Beedrill) para probar.
        for i in range(1, 16):
            try:
                # 1. Obtener objeto Pokemon (stats, tipos, altura...)
                p = pb.pokemon(i)

                # 2. Obtener objeto Species (para descripción, legendario, color...)
                s = p.species

                #Obtener Tipos
                tipos = []

                for t in p.types:
                    tipo_obj = t.type  # Objeto Type
                    nombre_tipo = tipo_obj.name.capitalize()  # fallback en inglés

                    for n in tipo_obj.names:
                        if n.language.name == 'es':
                            nombre_tipo = n.name
                            break

                    tipos.append(nombre_tipo)

                #Obtener cadena evolutiva
                chain = s.evolution_chain.chain

                def recorrer(chain, lista):
                    lista.append(chain.species.name)
                    for evo in chain.evolves_to:
                        recorrer(evo, lista)

                todos = []
                recorrer(chain, todos)

                idx = todos.index(p.name)

                preevoluciones = todos[:idx]
                evoluciones = todos[idx + 1:]

                preevoluciones = [pr.capitalize() for pr in preevoluciones]
                evoluciones = [ev.capitalize() for ev in evoluciones]

                # Procesar Descripción (Busca la primera en español, o usa inglés por defecto)
                descripcion = "Sin descripción"
                for entry in s.flavor_text_entries:
                    if entry.language.name == 'es':
                        descripcion = entry.flavor_text.replace("\n", " ")
                        break

                # Construir diccionario limpio
                datos_poke = {
                    "id": p.id,
                    "nombre": p.name.capitalize(),
                    "altura": p.height / 10.0,  # Convertir decímetros a metros
                    "peso": p.weight / 10.0,  # Convertir hectogramos a kg
                    "tipos": tipos,  # Lista de strings ['Planta', 'Veneno']
                    "preevoluciones": preevoluciones,
                    "evoluciones": evoluciones,
                    "descripcion": descripcion,
                    "legendario": s.is_legendary,
                    "region": "Kanto"  # Asumimos Kanto para la gen 1
                }

                lista_datos.append(datos_poke)
                print(f"Descargado: {p.name}")

            except Exception as e:
                print(f"Error descargando pokemon ID {i}: {e}")
                continue

        print("--- CARGA DE API COMPLETADA ---")
        return lista_datos

    @staticmethod
    def cargarTiposEfectos() -> List[Dict[str, Any]]:
        print("--- CONECTANDO CON POKEAPI (Esto puede tardar unos segundos) ---")
        print("--- CARGANDO TIPOS Y EFECTOS ---")
        lista_datos = []

        # Traducir los nombres de los tipos a español
        def nombre_tipo_es(tipo):
            # Asegurar que tenemos el Type completo
            if not hasattr(tipo, "names"):
                tipo = pb.type_(tipo.name)

            for n in tipo.names:
                if n.language.name == 'es':
                    return n.name
            return tipo.name.capitalize()

        for tipo_id in range(1, 19):
            try:
                tipo = pb.type_(tipo_id)

                descripcion = "Tipo elemental"

                nombre = nombre_tipo_es(tipo)

                #Cargamos los efectos eficaces, débiles y nulos de cada tipo
                eficaz = [nombre_tipo_es(t) for t in tipo.damage_relations.double_damage_to]
                debil = [nombre_tipo_es(t) for t in tipo.damage_relations.double_damage_from]
                sin_efecto = [nombre_tipo_es(t) for t in tipo.damage_relations.no_damage_to]
                lista_datos.append({
                    "nombre": nombre,
                    "descripcion": descripcion,
                    "eficaz": eficaz,
                    "debil": debil,
                    "sin_efecto": sin_efecto
                })
                print(f"Descargado: {nombre}")
            except Exception as e:
                print(f"Error descargando tipo ID {tipo_id}: {e}")
                continue
        return lista_datos