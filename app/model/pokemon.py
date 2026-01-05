import json
import sqlite3

class Pokemon:
    def __init__(self, pokemon_id=0, nombre_custom="", rareza=0.0,
                 shiny=False, altura=0.0, peso=0.0, especie="", imagen=""):
        self.pokemon_id = pokemon_id
        self.nombre_custom = nombre_custom
        self.rareza = rareza
        self.shiny = shiny
        self.altura = altura
        self.peso = peso
        self.especie = especie
        self.imagen = imagen

    def getInfo(self):
        datos = {
            "pokemon_id": self.pokemon_id,
            "nombre_custom": self.nombre_custom,
            "rareza": self.rareza,
            "shiny": self.shiny,
            "altura": self.altura,
            "peso": self.peso,
            "especie": self.especie,
            "imagen": self.imagen
        }
        return datos
        #return json.dumps(datos, indent=4)

    def clonarPokemon(self):
        return Pokemon(
            self.pokemon_id, self.nombre_custom, self.rareza,
            self.shiny, self.altura, self.peso, self.especie,
            self.imagen
        )
