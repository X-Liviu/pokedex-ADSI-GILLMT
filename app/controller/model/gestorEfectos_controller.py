import json
class GestorEfectos:

    def __init__(self, efectos: list):
        self.efectos = efectos

    def obtenerEfectosEficaces(self, nombreTipo):
        datos = []
        for efecto in self.efectos :
            if efecto.esFuerte(nombreTipo) :
                datos.append(efecto.tipoDefensor)
        return json.dumps(datos, indent=4)

    def obtenerEfectosDebiles(self, nombreTipo):
        datos = []
        for efecto in self.efectos :
            if efecto.esDebil(nombreTipo) :
                datos.append(efecto.tipoDefensor)
        return json.dumps(datos, indent=4)