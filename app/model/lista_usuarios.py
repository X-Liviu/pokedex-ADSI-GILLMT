from typing import List
from app.model.usuario_ranking import UsuarioRanking
from app.model.utils.custom_types import Custom_types

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

            nuevo: UsuarioRanking = elemento
            # Caso en el que es el nuevo usuario es el mas pequeino de todos

            if parar:
                nuevo = elemento
                while indice < longitud:
                    actual = self.usuarios[indice]
                    self.usuarios[indice] = nuevo
                    nuevo = actual
                    indice += 1

            self.usuarios.append(nuevo)

    def get_index(self, p_nombre: str) -> int:
        resultado: int = -1
        indice: int = 0
        longitud: int = len(self.usuarios)

        while indice < longitud and resultado == -1:
            usuario_actual = self.usuarios[indice]

            if usuario_actual.es_mi_nombre(p_nombre):
                resultado = indice
            else:
                indice += 1

        return resultado

    def to_dict(self, p_nombre: str) -> Custom_types.Ranking.Usuarios:
        resultado: Custom_types.Ranking = {p_nombre: []}

        for indice, usuario in enumerate(self.usuarios):
            usuario_diccionario = usuario.to_dict()
            usuario_actual = { "nombre" : usuario_diccionario["nombre"], "rareza" : usuario_diccionario["rareza"], "puesto" : indice + 1 }

            resultado[p_nombre].append(usuario_actual)

        return resultado