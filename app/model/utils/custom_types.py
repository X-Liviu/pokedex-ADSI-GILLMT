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

        @classmethod
        def print(cls, value) -> None:
            print(cls.toString(value))

    class Testing:
        class EsMiNombre:
            NO_ERROR: int = 0
            SAME_NAME_ERROR: int = 1
            DIFFERENT_NAME_ERROR: int = 2

            @classmethod
            def toString(cls, value) -> str:
                resultado: str = "NOT POSSIBLE"
                if value == cls.NO_ERROR:
                    resultado = "NO ERROR"
                elif value == cls.SAME_NAME_ERROR:
                    resultado = "SAME NAME ERROR"
                elif value == cls.DIFFERENT_NAME_ERROR:
                    resultado = "DIFFERENT NAME ERROR"

                return resultado

            @classmethod
            def print(cls, value) -> None:
                print(cls.toString(value))

        class AddRareza:
            NO_ERROR: int = 0
            SUBTRACTION_ERROR: int = 1
            ADDITION_ERROR: int = 2

            @classmethod
            def toString(cls, value) -> str:
                resultado: str = "NOT POSSIBLE"
                if value == cls.NO_ERROR:
                    resultado = "NO ERROR"
                elif value == cls.SUBTRACTION_ERROR:
                    resultado = "SUBTRACTION ERROR"
                elif value == cls.ADDITION_ERROR:
                    resultado = "ADDITION ERROR"

                return resultado

            @classmethod
            def print(cls, value) -> None:
                print(cls.toString(value))

        class Compare:
            NO_ERROR: int = 0
            GREATER_THAN_ERROR: int = 1
            LOWER_THAN_ERROR: int = 2
            EQUAL_TO_ERROR: int = 3

            @classmethod
            def toString(cls, value) -> str:
                resultado: str = "NOT POSSIBLE"
                if value == cls.NO_ERROR:
                    resultado = "NO ERROR"
                elif value == cls.GREATER_THAN_ERROR:
                    resultado = "GREATER THAN ERROR"
                elif value == cls.LOWER_THAN_ERROR:
                    resultado = "SLOWER THAN ERROR"
                elif value == cls.EQUAL_TO_ERROR:
                    resultado = "EQUAL TO ERROR"

                return resultado

            @classmethod
            def print(cls, value) -> None:
                print(cls.toString(value))

    class SingletonError(Exception):
        pass