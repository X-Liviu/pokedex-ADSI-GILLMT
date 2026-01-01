class PokeDex:
    _instance = None  # Aquí guardaremos la instancia única

    def __init__(self, listaEspecies: list):
        # Si ya existe una instancia, evitamos que se cree otra por error
        if PokeDex._instance is not None:
            raise Exception("Esta clase es un Singleton. Usa get_instance()")

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