from typing import List
from app.model.usuario_ranking import UsuarioRanking
from app.utils.custom_types import Custom_types

class ListaUsuarios:
    def __init__(self):
        self.usuarios: List[UsuarioRanking] = []

    def insercion_ordenada(self, elemento: UsuarioRanking) -> None:
        # pre: elemento no esta en la lista
        longitud: int = len(self.usuarios)

        if longitud == 0:
            self.usuarios.append(elemento)
        else:
            indice: int = 0
            parar: bool = False

            while indice < longitud and not parar:
                usuario_actual = self.usuarios[indice]

                if usuario_actual.compare(elemento) == -1:
                    parar = not parar
                else:
                    indice += 1

            if parar:
                nuevo = elemento
                while indice < longitud:
                    actual = self.usuarios[indice]
                    self.usuarios[indice] = nuevo
                    nuevo = actual
                    indice += 1

                self.usuarios.append(nuevo)

    def to_dict(self, p_nombre: str) -> Custom_types.Ranking.Usuarios:
        return {
            p_nombre:
            [usuario.to_dict() for usuario in self.usuarios]
        }