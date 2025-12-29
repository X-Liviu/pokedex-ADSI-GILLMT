import sqlite3
from typing import List

from app.model.lista_usuarios import ListaUsuarios
from app.model.usuario_ranking import UsuarioRanking
from app.utils.custom_types import Custom_types
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
    def getMyRanking(cls, db: Connection) -> Ranking:
        if cls.myRanking == None:
            Ranking(db)
        return cls.myRanking

    def mostrarUsuarios(self) -> Custom_types.Ranking.Usuarios:
        """
        pre:
        post: Devuelve un diccionario con todos los usuarios existentes
        en la base de datos en orden de mas rareza a menos rareza
        """
        resultado: ListaUsuarios = None

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
            resultado = ListaUsuarios()

            usuario_actual: UsuarioRanking = UsuarioRanking("", 0)

            for fila in resultado_sql:

                if not usuario_actual.es_mi_nombre(fila["NombreUsuario"]):
                    if not usuario_actual.es_mi_nombre(""):
                        resultado.insercion_ordenada(usuario_actual)

                    usuario_actual = UsuarioRanking(fila["Nombre"], 0)

                usuario_actual.add_rareza(int(fila["Rareza"]))

            resultado.insercion_ordenada(usuario_actual)

        return resultado.to_dict("usuarios")

    def mostrarUsuario(self, pNombreUsuario: str) -> Custom_types.Ranking.Usuario:
        """
        pre: "pNombreUsuario" no esta vacio
        post: Dado un nombre de usuario, devuelve un diccionario con
        su nombre, una lista de pokemon que usa y sus nombres no comunes
        correspondientes.
        """
        resultado: Custom_types.Ranking.Usuario = None
        sentence: str = """
        SELECT
        NombreEspecie, NombreCustom
        from Usuario
        inner join Equipo
        on Usuario.NombreUsuario = Equipo.NombreUsuario
        inner join PokemonEnEquipo
        on Equipo.idEquipo = PokemonEnEquipo.idEquipo
        inner join Pokemon
        on PokemonEnEquipo.idPokemon = Pokemon.idPokemon
        WHERE Usuario.NombreUsuario = ?;
        """

        resultado_sql: List[sqlite3.Row] = self.bd.select(sentence, (pNombreUsuario,))

        if len(resultado_sql) > 0:
            resultado = {"nombre": pNombreUsuario, "equipoEspecie": [], "equipoCustom": []}

            for fila in resultado_sql:
                resultado["equipoEspecie"].append(fila["NombreEspecie"])
                resultado["equipoCustom"].append(fila["NombreCustom"])

        return resultado