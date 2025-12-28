from app.controller.model.pokemon_controller import Pokemon


class Equipo:
    def __init__(self, numEquipo: int, db):
        self.numEquipo = numEquipo
        self.lista_pokemon = []
        self.db = db

    def esEsteEquipo(self, num):
        return self.numEquipo == num

    def tiene6(self):
        return len(self.lista_pokemon) == 6

    def addPokemon(self, nombreEspecie, nombrePokemon):
        newPokemon = Pokemon()
        """
        El id se compone del nº del equipo al que se añade + 
        la posicion del pokemon en la lista del equipo
        """
        nuevoId = int(str(self.numEquipo) + str(len(self.lista_pokemon) + 1))
        newPokemon.pokemon_id = nuevoId
        newPokemon.nombre_custom = nombrePokemon
        newPokemon.nombre_especie = nombreEspecie

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

        return resumen_equipo

    def borrarPokemon(self, idPokemon):
        self.lista_pokemon = [p for p in self.lista_pokemon if p.pokemon_id != idPokemon]

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
