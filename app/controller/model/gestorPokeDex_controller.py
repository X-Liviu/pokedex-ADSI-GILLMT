import json
class gestorPokeDex() :
    def __init__(self, listaPokeDex: list) :
        self.listaPokedex = listaPokeDex

    def obtenerEfectos(self, nombreEspecie) :
        laEspecie = self.buscarEspecie(nombreEspecie)
        if laEspecie != None :
            datos = {"Efectos contra los que es fuerte": laEspecie.esFuerteContra(),
                     "Efectos contra los que es débil": laEspecie.esDebilContra()}
            return json.dumps(datos, indent=4)
        else:
            return -1

    def buscarEspecie(self, nombreEspecie) :
        for pokedex in self.listaPokedex :
            laEspecie = pokedex.buscarEspecie(nombreEspecie)
            if laEspecie != None :
                return laEspecie
        return None

    def caracteristicasPokemon(self, nombreEspecie) :
        laEspecie = self.buscarEspecie(nombreEspecie)
        if laEspecie != None :
            return laEspecie.getInfo()
        else:
            return -1

    def cadenaEvolutiva(self, nombreEspecie) :
        laEspecie = self.buscarEspecie(nombreEspecie)
        if laEspecie != None :
            return laEspecie.cadenaEvolutiva()
        else:
            return -1