from typing import Dict, List, Any

class Custom_types:
    class Ranking:
        Usuario = Dict[str, Any] # Asginacion de tipos de datos. Como el typedef en C
        Usuarios = Dict[str, List[Usuario]]

    class SingletonError(Exception):
        pass