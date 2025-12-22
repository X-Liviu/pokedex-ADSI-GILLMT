class Equipo:
    def __init__(self, numEquipo: int):
        self.numEquipo = numEquipo
        self.lista_pokemon = []

    def esEsteEquipo(self, num):
        return self.numEquipo == num

    def tiene6(self):
        return len(self.lista_pokemon) == 6