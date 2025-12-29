from typing import Dict, List, Any

class Custom_types:
    class Ranking:
        Usuario = Dict[str, Any] # Asginacion de tipos de datos. Como el typedef en C
        Usuarios = Dict[str, List[Usuario]]

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