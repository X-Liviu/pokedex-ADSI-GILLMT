import sqlite3
from typing import List
import pokebase

from app.model.lista_usuarios import ListaUsuarios
from app.model.usuario_ranking import UsuarioRanking
from app.model.utils.custom_types import Custom_types
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

    def mostrarRanking(self) -> Custom_types.Ranking.Usuarios:
        """
        pre:
        post: Devuelve un diccionario con todos los usuarios existentes
        en la base de datos en orden de mas rareza a menos rareza
        """
        return self._get_lista_usuarios().to_dict("usuarios")

    def _get_lista_usuarios(self) -> ListaUsuarios:
        sentence: str = """
                        SELECT Usuario.NombreUsuario, Pokemon.Rareza
                        from Usuario
                                 inner join Equipo
                                            on Usuario.NombreUsuario = Equipo.NombreUsuario
                                 inner join PokemonEnEquipo
                                            on Equipo.idEquipo = PokemonEnEquipo.idEquipoInterno
                                 inner join Pokemon
                                            on Pokemon.idPokemon = PokemonEnEquipo.idPokemon
                        Order By Usuario.NombreUsuario; \
                        """

        resultado_sql: List[sqlite3.Row] = self.bd.select(sentence)
        resultado = ListaUsuarios() #He cambiado esto, para que en caso de que no sea capaz de obtener los usuarios de la BD, que no explote y de Internal Server Error - Liviu (15:28 - 11/01/2026)

        if len(resultado_sql) > 0:
            resultado = ListaUsuarios()

            usuario_actual: UsuarioRanking = UsuarioRanking("", 0)

            for fila in resultado_sql:

                if not usuario_actual.es_mi_nombre(fila["NombreUsuario"]):
                    if not usuario_actual.es_mi_nombre(""):
                        resultado.insercion_ordenada(usuario_actual)

                    usuario_actual = UsuarioRanking(fila["NombreUsuario"], 0)

                usuario_actual.add_rareza(int(fila["Rareza"]))

            resultado.insercion_ordenada(usuario_actual)

        return resultado

    def _get_puesto_by_nombre(self, nombre: str) -> int:
        lista_actual: ListaUsuarios = self._get_lista_usuarios()
        return ( lista_actual.get_index(nombre) + 1)

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
        on Equipo.idEquipo = PokemonEnEquipo.idEquipoInterno
        inner join Pokemon
        on PokemonEnEquipo.idPokemon = Pokemon.idPokemon
        WHERE Usuario.NombreUsuario = ?;
        """

        resultado_sql: List[sqlite3.Row] = self.bd.select(sentence, (pNombreUsuario,))

        if len(resultado_sql) > 0:
            puesto_actual: int = self._get_puesto_by_nombre(pNombreUsuario)
            resultado = {"nombre": pNombreUsuario, "equipoEspecie": [], "equipoCustom": [], "fotoPokemon": [],"puesto": puesto_actual}

            for fila in resultado_sql:
                resultado["equipoEspecie"].append(fila["NombreEspecie"])
                resultado["equipoCustom"].append(fila["NombreCustom"])
                sprite_actual = pokebase.pokemon(fila["NombreEspecie"].lower()).sprites.front_default
                # TODO: La linea sprite actual hay que cambiarla a una llamada de la Pokedex
                resultado["fotoPokemon"].append(sprite_actual)

        return resultado