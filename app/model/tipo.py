class Tipo:
    def __init__(self, nombre: str, descripcion: str) :
        self.nombre = nombre
        self.descripcion = descripcion

#para convertir a diccionario
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }