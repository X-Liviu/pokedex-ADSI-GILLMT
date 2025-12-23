import json
class gestorPokeDex() :
    def __init__(self, listaPokeDex: list) :
        self.listaPokedex = listaPokeDex

    def obtenerEfectos(self, nombreEspecie) :
        laEspecie = self.buscarEspecie(nombreEspecie)
        if laEspecie != None :
            datos = [laEspecie.esFuerteContra(),laEspecie.esDebilContra()]
            return json.dumps(datos, indent=4)

    def buscarEspecie(self, nombreEspecie) :
        for pokedex in self.listaPokedex :
            laEspecie = pokedex.buscarEspecie(nombreEspecie)
            if laEspecie != None :
                return laEspecie
        return None