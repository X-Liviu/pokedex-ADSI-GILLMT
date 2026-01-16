from app.database.connection import Connection
from app.model.efecto import Efecto


class gestorEfectos: pass

class gestorEfectos:
    myGestorEfectos: gestorEfectos = None

    def __init__(self, efectos: list):
        self.efectos = efectos

    @classmethod
    def getGestorEfectos(cls, efectos=None):
        if cls.myGestorEfectos is None:
            if efectos is None:
                efectos = []
            cls.myGestorEfectos = gestorEfectos(efectos)
        return cls.myGestorEfectos

    def obtenerEfectosEficaces(self, nombreTipo):
        #Devuelve los efectos contra los que el tipo es fuerte
        datos = []
        for efecto in self.efectos :
            if efecto.esFuerte(nombreTipo) :
                datos.append(efecto.tipoDef)
        return datos

    def obtenerEfectosDebiles(self, nombreTipo):
        #Devuelve los efectos contra los que el tipo es débil
        datos = []
        for efecto in self.efectos :
            if efecto.esDebil(nombreTipo) :
                datos.append(efecto.tipoDef)
        return datos

    def anadirEfecto (self, tipoAtac, tipoDef, efecto):
        nuevo = Efecto(tipoAtac, tipoDef, efecto)
        self.efectos.append(nuevo)

    def reiniciarEfectos(self):
        """
        Vacía la lista de especies para evitar duplicados al recargar datos.
        """
        self.efectos = []
        print("[DEBUG] Efectos reiniciados (Memoria limpia).")