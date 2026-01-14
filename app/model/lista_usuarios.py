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

    def get_users_as_dict(self) -> Custom_types.Ranking.Usuario:
        for usuario_actual in self.usuarios:
            yield usuario_actual.to_dict() # Esto es un iterador

        """
        EXPLICACION:
        get_to_dict se ha convertido en un generador. Cuando se
        hace una llamada a un generador su ejecucion se PAUSA
        cuando hay un yield. La ejecucion del generador continua
        desde el ultimo yield en el que se pauso. Un generador
        es un objeto y siempre que se vaya a usar uno, requiere
        inicializarse. Si se usa en un bucle for devolvera el
        valor al lado de yield en cada ciclo del for externo.
        No se ejecutan dos bucles seguidos, sino que se ejecuta
        el bucle "a la vez". No se si conocias esto, si no lo
        conocias lo intento explicar mas detalladamente.
        """