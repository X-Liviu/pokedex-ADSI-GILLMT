class gestorUsuario:
    def __init__(self, usuario) :
        self.usuario = usuario
        pass

    def noEsNull(self):
        return self.usuario is None

    def crearEquipo(self) :
        return self.usuario.addEquipo()

    def tieneEquipos(self) :
        return self.usuario.tieneEquipos()

    def getListaEquipos(self) :
        return self.usuario.exportarEquiposJSON()