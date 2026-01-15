class Efecto:
    def __init__(self, tipoAtac: str, tipoDef: str, efecto: str) :
        self.tipoAtac = tipoAtac
        self.tipoDef = tipoDef
        self.efecto = efecto

    def esFuerte(self, nombreTipo) :
        return (nombreTipo == self.tipoAtac) and (self.efecto == "Eficaz")

    def esDebil(self, nombreTipo) :
        return (nombreTipo == self.tipoAtac) and (self.efecto == "Débil")

