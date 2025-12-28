from app.controller.model.usuario_controller import Usuario

class gestorCopiasEquipo:
    def __init__(self):
        self.copiaOriginal = None

    def clonarEquipo(self, usuario, numEquipo) :
        equipoOrigianl = usuario.buscarEquipo(numEquipo)
        self.copiaOriginal = equipoOrigianl.clonar()