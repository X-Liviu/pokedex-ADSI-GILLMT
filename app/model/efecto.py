class Efecto:
    def __init__(self, tipoAtacante: str, tipoDefensor: str, efecto: str) :
        self.tipoAtacante = tipoAtacante
        self.tipoDefensor = tipoDefensor
        self.efecto = efecto

    def esFuerte(self, nombreTipo) :
        return (nombreTipo == self.tipoAtacante) and (self.efecto == "Eficaz")

    def esDebil(self, nombreTipo) :
        return (nombreTipo == self.tipoAtacante) and (self.efecto == "Debil")

