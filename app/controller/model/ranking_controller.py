import sqlite3
from typing import List
from app.custom_types import Custom_types
from app.database.connection import Connection

class Ranking: pass
# Python no reconoce la clase hasta que no termina toda la implementacion

class Ranking:
    myRanking: Ranking = None

    def __init__(self, bd: Connection):
        if Ranking.myRanking == None:
            self.bd: Connection = bd
            Ranking.myRanking = self
        else:
            raise Custom_types.SingletonError()

    @classmethod # Igual que los metodos estaticos de Java
    def getMyRanking(cls) -> Ranking:
        return cls.myRanking

    def mostrarUsuarios(self) -> Custom_types.Ranking.Usuarios:
        resultado: Custom_types.Ranking.Usuarios = None
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
            usuario_actual: Custom_types.Ranking.Usuario = {"nombre": "", "rareza": -1.0, "puesto": -1}
            usuario_actual["nombre"] = fila["nombre"]
            usuario_actual["rareza"] = fila["rareza"]
            usuario_actual["puesto"] = fila["puesto"]

            resultado.get("usuarios").append(usuario_actual)

        return resultado
        """
        El metodo dump transforma el diccionario en un objeto JSON y lo guarda en un archivo,
        mientras que el metodo dumps transforma el diccionario en un objeto JSON, pero este
        esta contenido en un string
        """

    def mostrarUsuario(self, pNombreUsuario: str) -> Custom_types.Ranking.Usuario:
        resultado: Custom_types.Ranking.Usuario = None
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

        return resultado