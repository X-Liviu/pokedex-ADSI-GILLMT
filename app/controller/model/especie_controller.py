
class Especie:
    def __init__(self, nombre: str, descripcion: str, legendario: bool, alturaMedia: float, pesoMedio : float, tipos: list):
        self.nombre = nombre
        self.descripcion = descripcion
        self.legendario = legendario
        self.alturaMedia = alturaMediaç
        self.pesoMedio = pesoMedio
        self.tipos = tipos

    def esEsta(self, nombreEspecie):
        return self.nombre == nombreEspecie

    def esFuerteContra(self):
        datos = []
        for tipo in self.tipos :
            datos.append(gestorEfectos.obtenerEfectosEficaces(tipo.nombre))
        return json.dumps(datos, indent=4)

    def esDebilContra(self):
        datos = []
        for tipo in self.tipos :
            datos.append(gestorEfectos.obtenerEfectosDebiles(tipo.nombre))
        return json.dumps(datos, indent=4)