from typing import Dict, List, Any

class Custom_types:
    class Ranking:
        Usuario = Dict[str, Any] # Asginacion de tipos de datos. Como el typedef en C
        Usuarios = Dict[str, List[Usuario]]

        class ListaUsuarios:
            def __init__( self ):
                self.usuarios = []

            def insercion_ordenada(self, elemento) -> None:
                # pre: elemento no esta en la lista
                longitud: int = len(self.usuarios)

                if longitud == 0:
                    self.usuarios.append({"nombre": elemento["nombre"], "rareza": elemento["rareza"]})
                else:
                    indice: int = 0
                    parar: bool = False

                    while indice < longitud and not parar:
                        usuario_actual = self.usuarios[indice]

                        if usuario_actual["rareza"] < elemento["rareza"]:
                            parar = not parar
                        else:
                            indice += 1

                    if parar:
                        nuevo = elemento
                        while indice < longitud:
                            actual = self.usuarios[indice]
                            self.usuarios[indice] = {"nombre": nuevo["nombre"], "rareza": nuevo["rareza"]}
                            nuevo = actual
                            indice += 1

                        self.usuarios.append({"nombre": nuevo["nombre"], "rareza": nuevo["rareza"]})

            def to_dict(self, p_nombre: str) -> Dict[str, List[Any]]:
                return { p_nombre: self.usuarios }

    class VerUsuario:
        NO_SOLICITADO: int = 0
        AMIGO_NUEVO: int = 1
        AMIGO_ERROR: int = 2

        @classmethod
        def toString(cls, value) -> str:
            resultado: str = "NOT POSSIBLE"
            if value == cls.NO_SOLICITADO:
                resultado = "NO SOLICITADO"
            elif value == cls.AMIGO_NUEVO:
                resultado = "AMIGO NUEVO"
            elif value == cls.AMIGO_ERROR:
                resultado = "AMIGO ERROR"

            return resultado

    class SingletonError(Exception):
        pass