import json
class Pokemon:
    def __init__(self, pokemon_id: int, nombre_custom: str, rareza: float,
                 shiny: bool, altura: float, peso : float, especie: str, imagen: str,
                 db):
        self.pokemon_id = pokemon_id
        self.nombre_custom = nombre_custom
        self.rareza = rareza
        self.shiny = shiny
        self.altura = altura
        self.peso = peso
        self.especie = especie
        self.imagen = imagen
        self.db = db

    def getInfo(self):
        datos = {
            "pokemon id": self.pokemon_id,
            "nombre_custom": self.nombre_custom,
            "rareza": self.rareza,
            "shiny": self.shiny,
            "altura": self.altura,
            "peso": self.peso,
            "especie": self.especie,
            "imagen": self.imagen
        }
        return json.dumps(datos, indent=4)

    def guardarPokemon(self, numEquipo: int):
        self.db.insert(
            sentence="INSERT INTO Pokemon (idPokemon, NombreCustom, Rareza, Shiny, Altura, Peso, NombreEspecie) VALUES (%self.pokemon_id%, %self.nombre_custom%, %self.rareza%, %self.shiny%, %self.altura%, %self.peso%, %self.especie%)"
        )
        self.db.insert(
            sentence="INSERT INTO PokemonEnEquipo (idEquipo, idPokemon) VALUES (%numEquipo%, %self.pokemon_id%)"
        )