from app.controller.model.usuario_controller import Usuario
from app.controller.model.pokemon_controller import Pokemon
from app.controller.model.equipo_controller import Equipo

class gestorCopiasEquipo:
    def __init__(self):
        self.copiaOriginal = None

    def clonarEquipo(self, usuario, numEquipo) :
        equipoOrigianl = usuario.buscarEquipo(numEquipo)
        self.copiaOriginal = equipoOrigianl.clonar()

    def compararCopiasEliminar(self, usuario, numEquipo) :
        equipoEditado = usuario.buscarEquipo(numEquipo)
        for p in self.copiaOriginal.lista_pokemon :
            if not equipoEditado.buscarPokemon(p.pokemon_id):
                p.borrarPokemonBD()

    def compararCopiasAniadir(self, usuario, numEquipo) :
        equipoEditado = usuario.buscarEquipo(numEquipo)
        for p in equipoEditado.lista_pokemon :
            if not self.copiaOriginal.buscarPokemon(p.pokemon_id):
                p.guardarPokemon()