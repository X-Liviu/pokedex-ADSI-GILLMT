import json

from app.controller.model.gestorEfectos_controller import gestorEfectos


class Especie:
    def __init__(self, nombre: str, descripcion: str, legendario: bool, alturaMedia: float, pesoMedio : float, movimientos: list, tipos: list, imagen: str, evoluciones: list, preevoluciones: list):
        self.nombre = nombre
        self.descripcion = descripcion
        self.legendario = legendario
        self.alturaMedia = alturaMedia
        self.pesoMedio = pesoMedio
        self.movimientos = movimientos
        self.tipos = [t.nombre if hasattr(t,'nombre') else str(t) for t in tipos]
        self.imagen = imagen
        self.evoluciones = evoluciones
        self.preevoluciones = preevoluciones

    def esEsta(self, nombreEspecie):
        return self.nombre == nombreEspecie

    def getTipos(self):
        return self.tipos

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

    def cadenaEvolutiva(self):
        #Devuelve la cadena evolutiva de un Pokémon
        #Si la cadena solo se compone de un Pokémon
        if (len(self.preevoluciones) == 0) & (len(self.evoluciones) == 0):
            datos = {"Cadena evolutiva": self.nombre}
        #Si el Pokémon es la evolución de la cadena
        elif len(self.evoluciones) == 0 :
            datos = {"Cadena evolutiva": self.preevoluciones + [self.nombre]}
        #Si el Pokémon es la preevolución de la cadena
        elif len(self.preevoluciones) == 0 :
            datos = {"Cadena evolutiva": [self.nombre] + self.evoluciones}
        #Si el Pokémon tiene tanto evolución como preevolución
        else:
            datos = {"Cadena evolutiva": self.preevoluciones + [self.nombre] + self.evoluciones}
        return datos




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

