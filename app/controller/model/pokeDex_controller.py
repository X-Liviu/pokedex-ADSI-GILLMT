import json
from app.controller.model.especie_controller import Especie

class PokeDex:
    _instance = None  # Aquí guardaremos la instancia única

    def __init__(self, listaEspecies: list):
        # Si ya existe una instancia, evitamos que se cree otra por error
        if PokeDex._instance is not None:
            raise Exception("Esta clase es un Singleton. Usa get_instance()")

        #PRUEBAS TATA
        # especies_para_pokedex = [
        #     Especie(
        #         nombre="Pikachu",
        #         descripcion="Mantiene su cola en alto...",
        #         legendario=False,  # RECUERDA: 'legendario' en español
        #         alturaMedia=0.4,
        #         pesoMedio=6.0,
        #         movimientos=["Impactrueno"],
        #         tipos=["Eléctrico"],  # Palabras normales
        #         imagen="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
        #     ),
        #
        #     Especie(
        #         nombre="Eevee",
        #         descripcion="Posee una estructura genética...",
        #         legendario=False,  # CORREGIDO: de legendary a legendario
        #         alturaMedia=0.3,
        #         pesoMedio=6.5,
        #         movimientos=["Refuerzo"],
        #         tipos=["Normal"],
        #         imagen="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/133.png"
        #     )
        # ]
        # self.listaEspecies = especies_para_pokedex

        self.listaEspecies = listaEspecies
        PokeDex._instance = self

    @classmethod
    def get_instance(cls, listaEspecies=None):
        """
        Si no existe la Pokedex, la crea. Si ya existe, la devuelve.
        """
        if cls._instance is None:
            if listaEspecies is None:
                listaEspecies = []
            PokeDex(listaEspecies)
        return cls._instance

    def buscarEspecie(self, nombreEspecie):
        for especie in self.listaEspecies:
            if especie.esEsta(nombreEspecie):
                return especie
        return None

    def mostrarPokedex(self) -> str:
        lista_final = []
        for especie in self.listaEspecies:
            lista_final.append(especie.getInfo())

        return json.dumps(lista_final, indent=4)

    def getInfo(self, nombreEspecie: str) -> str:
        """
        Busca un Pokémon específico y devuelve su JSON
        """
        for especie in self.listaEspecies:
            if especie.nombre.lower() == nombreEspecie.lower():
                return json.dumps(especie.getInfo(), indent=4, ensure_ascii=False)
        return json.dumps({"error": "Pokémon no encontrado"})

    def filtrarPokedex(self, filtro: str, valor: str) -> str:
        lista_filtrada = []
        #bucle para cada especie pokemon
        for especie in self.listaEspecies:
            if especie.comprobarFiltroValor(filtro, valor):
                lista_filtrada.append(especie.getInfo())

        return json.dumps(lista_filtrada, indent=4)
