class gestorUsuario:
    def __init__(self, usuario) :
        self.usuario = usuario
        pass

    def tieneEquipos(self) :
        return self.usuario.tieneEquipos()

    def getListaEquipos(self) :
        return self.usuario.exportarEquiposJSON()