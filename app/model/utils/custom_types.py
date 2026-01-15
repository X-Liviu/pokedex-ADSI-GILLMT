from typing import Dict, List, Any

class Custom_types:
    class Ranking:
        # Diagrama de secuencia 1
        JSONCalificacionUsuario1 = Dict[str, Any] # Esto deberia ser {"usuario": String, "rareza": float}
        JSONCalificacionUsuario2 = Dict[str, Any] # Esto deberia ser {"usuario": String, "rareza": float, "puesto": int}
        JSONRanking = Dict[str, List[Any]] # Esto deberia ser Dict[str, List[JSONCalificacionUsuario1]]

        # Diagrama de secuencia 2
        JSONRankingUsuario = Dict[str, Any]
        """
        Esto deberia ser {"nombre": str,
                         "equipoEspecie": List,
                         "equipoCustom": List,
                         "fotoPokemon": List,
                         "puesto": int,
                         "estado_amigo": int
                         }
        """

    class GestorUsuario:
        JSONEstadoAmigo = Dict[str, bool]

    class PerfilUsuario:
        NO_AMIGO: int = 0
        SI_AMIGO: int = 1
        TU_MISMO: int = 2

        @classmethod
        def toString(cls, value) -> str:
            resultado: str = "NOT POSSIBLE"
            if value == cls.NO_AMIGO:
                resultado = "NO AMIGO"
            elif value == cls.TU_MISMO:
                resultado = "TU MISMO"
            elif value == cls.SI_AMIGO:
                resultado = "SI AMIGO"

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