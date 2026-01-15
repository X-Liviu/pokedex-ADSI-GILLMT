from app.database.connection import Connection
from app.model.efecto import Efecto


class gestorEfectos: pass

class gestorEfectos:
    myGestorEfectos: gestorEfectos = None

    def __init__(self, efectos: list, db):
        self.efectos = efectos
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

    def anadirEfecto (self, tipoAtac, tipoDef, efecto):
        nuevo = Efecto(tipoAtac, tipoDef, efecto)
        self.efectos.append(nuevo)