class Efecto:
    def __init__(self, tipoAtac: str, tipoDef: str, efecto: str) :
        self.tipoAtac = tipoAtac
        self.tipoDef = tipoDef
        self.efecto = efecto

    def esFuerte(self, nombreTipo) :
        #Indica si el tipo introducido es eficaz
        return (nombreTipo == self.tipoAtac) and (self.efecto == "Eficaz")

    def esDebil(self, nombreTipo) :
        #Indica si el tipo introducido es débil
        return (nombreTipo == self.tipoAtac) and (self.efecto == "Débil")

