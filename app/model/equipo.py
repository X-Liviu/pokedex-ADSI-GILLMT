import random

from app.model.pokemon import Pokemon
from app.controller.model.pokeDex_controller import PokeDex

class Equipo:
    def __init__(self, numEquipo: int):
        self.numEquipo = numEquipo
        self.lista_pokemon = []
        self.ultimo_id_pokemon = 0

    def esEsteEquipo(self, num):
        return self.numEquipo == num

    def tiene6(self):
        return len(self.lista_pokemon) == 6

    def addPokemon(self, nombreEspecie, nombrePokemon):
        # 1. Obtenemos la especie desde el Singleton PokeDex
        especie_obj = PokeDex.get_instance().buscarEspecie(nombreEspecie)

        if not especie_obj:
            print(f"Error: La especie {nombreEspecie} no existe.")
            return -1  # Especie no encontrada en la PokeDex

        for pokemon in self.lista_pokemon:
            if pokemon.nombre_custom == nombrePokemon :
                return -2
            elif pokemon.especie == nombreEspecie :
                return -3

        # Obtenemos el diccionario de la especie
        datos = especie_obj.getInfo()
        # 2. Generamos el ID único (Tu lógica de concatenar numEquipo + contador)
        self.ultimo_id_pokemon += 1
        nuevoId = int(str(self.numEquipo) + str(self.ultimo_id_pokemon))

        # 3. Probabilidad Shiny (10%)
        es_shiny = random.random() < 0.1

        # 4. Creación del objeto Pokemon
        newPokemon = Pokemon(
            pokemon_id=nuevoId,
            nombre_custom=nombrePokemon,
            rareza=datos.get("rareza", "Común"),
            shiny=es_shiny,
            altura=datos.get("alturaMedia", 0.0),
            peso=datos.get("pesoMedio", 0.0),
            especie=nombreEspecie,
            imagen=datos.get("imagen", ""),
        )

        self.lista_pokemon.append(newPokemon)
        return 1  # Éxito

    def mostrarInfoEquipo(self):
        resumen_equipo = []
        for pokemon in self.lista_pokemon:
            info_completa = pokemon.getInfo()

            info_filtrada = {
                "pokemon_id": info_completa["pokemon_id"],
                "nombre_custom": info_completa["nombre_custom"],
                "shiny": info_completa["shiny"],
                "especie": info_completa["especie"],
                "imagen": info_completa["imagen"]
            }

            resumen_equipo.append(info_filtrada)

        return resumen_equipo
        #return json.dumps(resumen_equipo)

    def borrarPokemon(self, idPokemon):
        # Convertimos ambos a string para asegurar que la comparación sea válida
        self.lista_pokemon = [p for p in self.lista_pokemon if str(p.pokemon_id) != str(idPokemon)]

    def buscarPokemon(self, idPokemon):
        for pokemon in self.lista_pokemon:
            if pokemon.pokemon_id == idPokemon:
                return True
        return False

    def clonar(self):
        nuevoEquipo = Equipo(self.numEquipo)
        nuevoEquipo.ultimo_id_pokemon = self.ultimo_id_pokemon
        for pokemon in self.lista_pokemon:
            nuevoPokemon = pokemon.clonarPokemon()
            nuevoEquipo.lista_pokemon.append(nuevoPokemon)

        return nuevoEquipo

    def restaurarEquipo(self, equipo):
        self.numEquipo = equipo.numEquipo
        self.ultimo_id_pokemon = equipo.ultimo_id_pokemon
        self.lista_pokemon = []
        for pokemon in equipo.lista_pokemon:
            self.lista_pokemon.append(pokemon.clonarPokemon())

    def getMejorPokemon(self):
        max = 0.0
        elPokemon = self.lista_pokemon[0]
        for Pokemon in range(1, len(self.lista_pokemon)):
            if max <= Pokemon.rareza:
                rareza = Pokemon.rareza
                elPokemon = Pokemon
        return elPokemon.getInfo()

    def addPokemon(self, nombreEspecie, nombrePokemon, datos_bd=None):
        """
        Paso 36aa: addPokemon.
        Soporta carga desde BD (datos_bd) o creación nueva (lógica original).
        """
        # 1. Obtenemos especie
        especie_obj = PokeDex.get_instance().buscarEspecie(nombreEspecie)
        if not especie_obj:
            return -1

        # Variables para construir el Pokemon
        nuevoId = 0
        rareza = 0.0
        es_shiny = False
        altura = 0.0
        peso = 0.0
        imagen = ""

        if datos_bd:
            # --- MODO CARGA (Desde BD) ---
            nuevoId = datos_bd['id_real']
            rareza = datos_bd['rareza']
            es_shiny = datos_bd['shiny']
            altura = datos_bd['altura']
            peso = datos_bd['peso']
            imagen = datos_bd['imagen']

            # Ajustamos el contador interno para no re-generar IDs duplicados en el futuro
            try:
                # Suponiendo que el ID es int. Si es compuesto, ajusta lógica.
                self.ultimo_id_pokemon += 1
            except:
                pass

        else:
            # --- MODO CREACIÓN (Nuevo, Random) ---
            # Validaciones de equipo lleno o duplicados solo si es NUEVO
            for p in self.lista_pokemon:
                if p.nombre_custom == nombrePokemon: return -2
                if p.especie == nombreEspecie: return -3

            datos_especie = especie_obj.getInfo()
            self.ultimo_id_pokemon += 1
            nuevoId = int(f"{self.numEquipo}{self.ultimo_id_pokemon}")  # Generación ID simple

            es_shiny = random.random() < 0.1
            rareza = datos_especie.get("rareza", 0.0)
            altura = datos_especie.get("alturaMedia", 0.0)
            peso = datos_especie.get("pesoMedio", 0.0)
            imagen = datos_especie.get("imagen", "")

        # Paso 37aa (Implícito): Crear y guardar en lista (memoria)
        newPokemon = Pokemon(
            pokemon_id=nuevoId,
            nombre_custom=nombrePokemon,
            rareza=rareza,
            shiny=es_shiny,
            altura=altura,
            peso=peso,
            especie=nombreEspecie,
            imagen=imagen
        )

        self.lista_pokemon.append(newPokemon)
        return 1
