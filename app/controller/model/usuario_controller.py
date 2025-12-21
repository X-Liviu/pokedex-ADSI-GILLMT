class Usuario:
    def __init__(self, nombre: str, apellido: str, nombre_usuario: str, correo: str, contrasena: str, rol: str, lista_equipos: list):
        self.nombre = nombre
        self.apellido = apellido
        self.nombre_usuario = nombre_usuario
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol
        self.lista_equipos = lista_equipos

    def buscarEquipo(self, numEquipo: int):
        for equipo in self.lista_equipos:
            if equipo.esEsteEquipo(numEquipo):
                return equipo
        return None