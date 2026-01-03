import json

from app.controller.model.gestorEfectos_controller import GestorEfectos


class Especie:
    def __init__(self, nombre: str, descripcion: str, legendario: bool, alturaMedia: float, pesoMedio : float, movimientos: list, tipos: list, imagen: str):
        self.nombre = nombre
        self.descripcion = descripcion
        self.legendario = legendario
        self.alturaMedia = alturaMedia
        self.pesoMedio = pesoMedio
        self.movimientos = movimientos
        self.tipos = tipos
        self.imagen = imagen

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
            "pesoMedio": self.pesoMedio,
            "movimientos": self.movimientos,
            "tipos": [t.to_dict() for t in self.tipos],
            "imagen": self.imagen
        }
        return datos
        #json.dumps(datos, indent=4)

    #TODO
    def cadenaEvolutiva(self):
        #Hay que ver como es la descripcion del Pokemo
        pass

    def comprobarFiltroValor(self, filtro: str, valor: str) -> bool:
        """
        Implementación del paso 2.1.1 del diagrama de filtros
        """
        # Pasamos la búsqueda a minúsculas para que no importe si escriben con mayúsculas
        valor_busqueda = valor.lower()

        if filtro == "nombre":
            # Comprueba si el texto buscado está dentro del nombre del Pokémon
            return valor_busqueda in self.nombre.lower()

        elif filtro == "tipo":
            # Comprueba si alguno de los tipos coincide con la búsqueda
            return any(valor == t.nombre.lower() for t in self.tipos)

        return False

