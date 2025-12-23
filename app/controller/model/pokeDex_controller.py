class PokeDex :
    def __init__(self, listaEspecies: list):
        self.listaEspecies = listaEspecies

        def buscarEspecie(self, nombreEspecie):
            for especie in self.listaEspeies:
                laEspecie = especie
                if laEspecie.esEsta(nombreEspecie):
                    return laEspecie
            return None