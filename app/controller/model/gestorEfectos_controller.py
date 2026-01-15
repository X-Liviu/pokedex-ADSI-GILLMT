from app.database.connection import Connection

class gestorEfectos: pass

class gestorEfectos:
    myGestorEfectos: gestorEfectos = None


    def __init__(self, db):
        self.db = db

    @classmethod
    def getGestorEfectos(cls, db=None):
        if cls.myGestorEfectos is None:
            cls.myGestorEfectos = gestorEfectos(db)
        return cls.myGestorEfectos

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