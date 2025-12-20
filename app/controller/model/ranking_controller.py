import json
import sqlite3
from typing import List, Any, Dict
from app.database.connection import Connection

class Ranking:
    Usuario = Dict[str, Any] # Asignaciones de tipos de dato. Equivalente a typedef de C

    def __init__(self):
        pass

    @staticmethod
    def mostrarUsuarios() -> str:
        resultado: Dict[str, List[Ranking.Usuario]] = None
        sentence: str = "select NombreUsuario, Rareza from Usuario inner join Equipo inner join PokemonEnEquipo inner join Pokemon Order By NombreUsuario;"

        conexion_ranking: Connection = Connection()
        resultado_sql: List[sqlite3.Row] = conexion_ranking.select(sentence)

        if len(resultado_sql) > 0:
            resultado = {"usuarios": []}

        for fila in resultado_sql:
            usuario_actual: Ranking.Usuario = {"nombre": "", "rareza": -1.0, "puesto": -1}
            usuario_actual["nombre"] = fila["nombre"]
            usuario_actual["rareza"] = fila["rareza"]
            usuario_actual["puesto"] = fila["puesto"]

            resultado.get("usuarios").append(usuario_actual)

        return json.dumps(resultado)
        """
        El metodo dump transforma el diccionario en un objeto JSON y lo guarda en un archivo,
        mientras que el metodo dumps transforma el diccionario en un objeto JSON, pero este
        esta contenido en un string
        """