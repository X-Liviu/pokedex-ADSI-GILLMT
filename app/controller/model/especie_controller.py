import json

from app.controller.model.gestorEfectos_controller import GestorEfectos


class Especie:
    def __init__(self, nombre: str, descripcion: str, legendario: bool, alturaMedia: float, pesoMedio : float, tipos: list):
        self.nombre = nombre
        self.descripcion = descripcion
        self.legendario = legendario
        self.alturaMedia = alturaMedia
        self.pesoMedio = pesoMedio
        self.tipos = tipos

    def esEsta(self, nombreEspecie):
        return self.nombre == nombreEspecie

    def esFuerteContra(self):
        datos = []
        for tipo in self.tipos :
            datos.append(GestorEfectos.obtenerEfectosEficaces(tipo.nombre))
        return json.dumps(datos, indent=4)

    def esDebilContra(self):
        datos = []
        for tipo in self.tipos :
            datos.append(GestorEfectos.obtenerEfectosDebiles(tipo.nombre))
        return json.dumps(datos, indent=4)

    def getInfo(self):
        datos = {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "legendario": self.legendario,
            "alturaMedia": self.alturaMedia,
            "pesoMedia": self.pesoMedio
        }
        json.dumps(datos, indent=4)

    #TODO
    def cadenaEvolutiva(self):
        #Hay que ver como es la descripcion del Pokemo
        pass
