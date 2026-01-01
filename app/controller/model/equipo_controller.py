import json
import random
import sqlite3

from app.controller.model.pokemon_controller import Pokemon
from app.controller.model.pokeDex_controller import PokeDex

class Equipo:
    def __init__(self, numEquipo: int, db):
        self.numEquipo = numEquipo
        self.lista_pokemon = []
        self.ultimo_id_pokemon = 0
        self.db = db

    def esEsteEquipo(self, num):
        return self.numEquipo == num

    def tiene6(self):
        return len(self.lista_pokemon) == 6

    def addPokemon(self, nombreEspecie, nombrePokemon):
        # 1. Obtenemos el JSON de la Pokedex
        # Asumimos que get_info ya devuelve un diccionario o hacemos el parse
        def addPokemon(self, nombreEspecie, nombrePokemon):
            # 1. Obtenemos la especie desde el Singleton PokeDex
            especie_obj = PokeDex.get_instance().buscarEspecie(nombreEspecie)

            if not especie_obj:
                print(f"Error: La especie {nombreEspecie} no existe.")
                return -1  # Especie no encontrada en la PokeDex

            # Obtenemos el diccionario/JSON de la especie
            info_especie = especie_obj.getInfo()
            datos = json.loads(info_especie) if isinstance(info_especie, str) else info_especie

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
                altura=datos.get("altura", 0.0),
                peso=datos.get("peso", 0.0),
                especie=nombreEspecie,
                # Seleccionamos imagen basándonos en el azar del shiny
                imagen=datos.get("imagen_shiny") if es_shiny else datos.get("imagen_normal"),
                db=self.db
            )

            self.lista_pokemon.append(newPokemon)
            return 1  # Éxito

    def guardarEquipo(self, numEquipo: int, nombre_usuario: str) :
        self.db.insert(
            sentence="INSERT INTO Equipo (idEquipo, NombreUsuario) VALUES (?,?)",
            parameters=(numEquipo, nombre_usuario)
        )

        for pokemon in self.lista_pokemon:
            pokemon.guardarPokemon(numEquipo)

    def mostrarInfoEquipo(self):
        resumen_equipo = []
        for pokemon in self.lista_pokemon:
            info_completa = pokemon.getInfo()

            info_filtrada = {
                "pokemon id": info_completa["pokemon id"],
                "nombre_custom": info_completa["nombre_custom"],
                "imagen": info_completa["imagen"]
            }

            resumen_equipo.append(info_filtrada)

        return json.dumps(resumen_equipo)

    def borrarPokemon(self, idPokemon):
        self.lista_pokemon = [p for p in self.lista_pokemon if p.pokemon_id != idPokemon]

    def buscarPokemon(self, idPokemon):
        for pokemon in self.lista_pokemon:
            if pokemon.pokemon_id == idPokemon:
                return True
        return False


    def clonar(self):
        nuevoEquipo = Equipo(self.numEquipo,self.db)
        nuevoEquipo.ultimo_id_pokemon = self.ultimo_id_pokemon
        for pokemon in self.lista_pokemon:
            nuevoPokemon = pokemon.clonarPokemon()
            nuevoEquipo.lista_pokemon.append(nuevoPokemon)

        return nuevoEquipo

    def restaurarEquipo(self, equipo):
        self.numEquipo = equipo.numEquipo
        self.ultimo_id_pokemon = equipo.ultimo_id_pokemon
        self.db = equipo.db
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
