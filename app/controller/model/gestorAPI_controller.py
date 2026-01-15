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
        print("--- CONECTANDO CON POKEAPI (Esto puede tardar unos segundos) ---")

        # Vamos a cargar del 1 al 15 (Bulbasaur a Beedrill) para probar.
        for i in range(1, 16):
            try:
                # 1. Obtener objeto Pokemon (stats, tipos, altura...)
                p = pb.pokemon(i)

                # 2. Obtener objeto Species (para descripción, legendario, color...)
                s = p.species

                tipos = []

                for t in p.types:
                    tipo_obj = t.type  # Objeto Type
                    nombre_tipo = tipo_obj.name.capitalize()  # fallback en inglés

                    for n in tipo_obj.names:
                        if n.language.name == 'es':
                            nombre_tipo = n.name
                            break

                    tipos.append(nombre_tipo)

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