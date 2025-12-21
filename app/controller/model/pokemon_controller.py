class Pokemon:
    def __init__(self, pokemon_id: int, nombre_custom: str, rareza: float, shiny: bool, altura: float, peso : float, especie: str):
        self.pokemon_id = pokemon_id
        self.nombre_custom = nombre_custom
        self.rareza = rareza
        self.shiny = shiny
        self.altura = altura
        self.peso = peso
        self.especie = especie
