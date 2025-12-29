from app.model.utils.custom_types import Custom_types

"""
-----------Usuario Ranking vs Usuario normal-----------
El primero solo es para manipular los datos del nombre
y el ranking dada la base de datos, ya que en el ranking
hemos considerado obtener los datos haciendo una consulta.
Entonces, Usuario normal no vale usar, porque seria por
objetos.
"""

class UsuarioRanking: pass

class UsuarioRanking:
    def __init__(self, nombre: str, rareza: int):
        self.nombre: str = nombre
        self.rareza: int = rareza

    def es_mi_nombre(self, nombre: str) -> bool:
        return nombre == self.nombre

    def add_rareza(self, rareza: int) -> None:
        self.rareza += rareza

    def to_dict(self) -> Custom_types.Ranking.Usuario:
        return {
            "nombre": self.nombre,
            "rareza": self.rareza
        }

    def compare(self, usuario: UsuarioRanking) -> int:
        resultado: int = 0

        if self.rareza > usuario.rareza:
            resultado = 1
        elif self.rareza < usuario.rareza:
            resultado = -1

        return resultado