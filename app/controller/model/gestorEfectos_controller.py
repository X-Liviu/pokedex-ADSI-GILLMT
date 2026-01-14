import json
class GestorEfectos:

    def __init__(self, efectos: list):
        self.efectos = efectos

    def obtenerEfectosEficaces(self, nombreTipo):
        datos = []
        for efecto in self.efectos :
            if efecto.esFuerte(nombreTipo) :
                datos.append(efecto.tipoDef)
        return datos

    def obtenerEfectosDebiles(self, nombreTipo):
        datos = []
        for efecto in self.efectos :
            if efecto.esDebil(nombreTipo) :
                datos.append(efecto.tipoDef)
        return datos