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
        self.tipos = [t.nombre if hasattr(t,'nombre') else str(t) for t in tipos]
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
            "tipos": self.tipos,
            "imagen": self.imagen
        }
        return datos

    #TODO
    def cadenaEvolutiva(self):
        #Hay que ver como es la descripcion del Pokemon
        pass

    def comprobarFiltroValor(self, filtro: str, valor: str) -> bool:
        """
        Implementación del paso 2.1.1 del diagrama de filtros
        """
        # Pasamos la búsqueda a minúsculas para que no importe si escriben con mayúsculas y quitamos los espacios
        valor_busqueda = valor.lower().strip()

        #limpiar tildes del valor
        valor_busqueda = valor_busqueda.replace("á", "a").replace("é", "e").replace("í","i").replace("ó","o").replace("ú","u")

        if filtro == "nombre":
            nombre = self.nombre.lower().replace("á", "a").replace("é", "e").replace("í","i").replace("ó","o").replace("ú","u")
            # Comprueba si el texto buscado está dentro del nombre del Pokémon
            return valor_busqueda in self.nombre.lower()

        elif filtro == "tipo":
            # Comprueba si alguno de los tipos coincide con la búsqueda
            for t in self.tipos:
                tipos=t.lower().replace("á", "a").replace("é", "e").replace("í","i").replace("ó","o").replace("ú","u")
                if valor_busqueda == tipos:
                    return True

        return False

