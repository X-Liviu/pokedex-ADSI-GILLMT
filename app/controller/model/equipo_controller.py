import json
import random
from app.controller.model.pokemon_controller import Pokemon
import sqlite3

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

    def addPokemon(self, nombreEspecie, nombrePokemon, pokedex):
        # 1. Obtenemos el JSON de la Pokedex
        # Asumimos que get_info ya devuelve un diccionario o hacemos el parse
        info_especie_json = pokedex.get_info(nombreEspecie)
        datos = json.loads(info_especie_json) if isinstance(info_especie_json, str) else info_especie_json

        if not datos:
            return -1  # Especie no encontrada

        # 2. Generamos el ID único histórico
        self.ultimo_id_pokemon += 1
        nuevoId = int(str(self.numEquipo) + str(self.ultimo_id_pokemon))

        # 3. Calculamos el Booleano Shiny (ej. 10% de probabilidad)
        es_shiny = random.random() < 0.1

        # 4. Creamos la instancia con los datos del JSON + el azar
        newPokemon = Pokemon(
            pokemon_id=nuevoId,
            nombre_custom=nombrePokemon,
            rareza=datos.get("rareza", 0.0),
            shiny=es_shiny,  # El booleano generado
            altura=datos.get("altura", 0.0),
            peso=datos.get("peso", 0.0),
            especie=nombreEspecie,
            # Elegimos la imagen del JSON según si es shiny o no
            imagen=datos.get("imagen_shiny") if es_shiny else datos.get("imagen_normal"),
            db=self.db
        )

        self.lista_pokemon.append(newPokemon)
        return 1

    def guardarEquipo(self, numEquipo: int, nombre_usuario: str) :
        self.db.insert(
            sentence="INSERT INTO Equipo (idEquipo, NombreUsuario) VALUES (%numEquipo%, %nombre_usuario%)"
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
        nuevoEquipo = Equipo(self.numEquipo)
        for pokemon in self.lista_pokemon:
            nuevoPokemon = pokemon.clonarPokemon()
            nuevoEquipo.lista_pokemon.append(nuevoPokemon)

        return nuevoEquipo

    def getMejorPokemon(self):
        max = 0.0
        elPokemon = self.lista_pokemon[0]
        for Pokemon in range(1, len(self.lista_pokemon)):
            if max <= Pokemon.rareza:
                rareza = Pokemon.rareza
                elPokemon = Pokemon
        return elPokemon.getInfo()
