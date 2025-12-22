import json
import sqlite3
from typing import List, Any, Dict
from app.database.connection import Connection

class RankingSingletonError(Exception):
    pass

class Ranking: pass

class Ranking:
    Usuario = Dict[str, Any] # Asignaciones de tipos de dato. Equivalente a typedef de C
    myRanking: Ranking = None

    def __init__(self, bd: Connection):
        if Ranking.myRanking == None:
            self.bd: Connection = bd
            Ranking.myRanking = self
        else:
            raise RankingSingletonError()

    @classmethod
    def getMyRanking(cls) -> Ranking:
        return cls.myRanking

    def mostrarUsuarios(self) -> str:
        resultado: Dict[str, List[Ranking.Usuario]] = None
        sentence: str = """
                        SELECT Usuario.NombreUsuario, Pokemon.Rareza
                        from Usuario
                        inner join Equipo
                        on Usuario.NombreUsuario = Equipo.NombreUsuario
                        inner join PokemonEnEquipo
                        on Equipo.idEquipo = PokemonEnEquipo.idEquipo
                        inner join Pokemon
                        on Pokemon.idPokemon = PokemonEnEquipo.idPokemon
                        Order By Usuario.NombreUsuario;
                        """

        resultado_sql: List[sqlite3.Row] = self.bd.select(sentence)

        if len(resultado_sql) > 0:
            resultado = {"usuarios": []}

        for fila in resultado_sql:
            resultado: Ranking.Usuario = {"nombre": "", "rareza": -1.0, "puesto": -1}
            resultado["nombre"] = fila["nombre"]
            resultado["rareza"] = fila["rareza"]
            resultado["puesto"] = fila["puesto"]

            resultado.get("usuarios").append(resultado)

        return json.dumps(resultado)
        """
        El metodo dump transforma el diccionario en un objeto JSON y lo guarda en un archivo,
        mientras que el metodo dumps transforma el diccionario en un objeto JSON, pero este
        esta contenido en un string
        """

    def mostrarUsuario(self, pNombreUsuario: str) -> str:
        resultado: Ranking.Usuario = None
        sentence: str = f"""
        SELECT
        NombreEspecie, NombreCustom
        from Usuario
        inner join Equipo
        on Usuario.NombreUsuario = Equipo.NombreUsuario
        inner join PokemonEnEquipo
        on Equipo.idEquipo = PokemonEnEquipo.idEquipo
        inner join Pokemon
        on PokemonEnEquipo.idPokemon = Pokemon.idPokemon
        WHERE Usuario.NombreUsuario = {pNombreUsuario};
        """

        resultado_sql: List[sqlite3.Row] = self.bd.select(sentence)

        if len(resultado_sql) > 0:
            resultado = {"nombre": pNombreUsuario, "equipoEspecie": [], "equipoCustom": []}

            for fila in resultado_sql:
                resultado.get("equipoEspecie").append(fila["equipoEspecie"])
                resultado.get("equipoCustom").append(fila["equipoCustom"])

        return json.dumps(resultado)

    def mostrarUsuario(self, pNombreUsuario: str) -> str:
        resultado: Ranking.Usuario = None
        sentence: str = f"""
        SELECT
        NombreEspecie, NombreCustom
        from Usuario
        inner join Equipo
        on Usuario.NombreUsuario = Equipo.NombreUsuario
        inner join PokemonEnEquipo
        on Equipo.idEquipo = PokemonEnEquipo.idEquipo
        inner join Pokemon
        on PokemonEnEquipo.idPokemon = Pokemon.idPokemon
        WHERE Usuario.NombreUsuario = {pNombreUsuario};
        """

        resultado_sql: List[sqlite3.Row] = self.bd.select(sentence)

        if len(resultado_sql) > 0:
            resultado = {"nombre": pNombreUsuario, "equipoEspecie": [], "equipoCustom": []}

            for fila in resultado_sql:
                resultado.get("equipoEspecie").append(fila["equipoEspecie"])
                resultado.get("equipoCustom").append(fila["equipoCustom"])

        return json.dumps(resultado)