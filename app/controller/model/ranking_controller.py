import json
import sqlite3
from typing import List
import pokebase

from app.controller.model.pokeDex_controller import PokeDex
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

    def mostrarRanking(self) -> Custom_types.Ranking.JSONRanking:
        """
        pre:
        post: Devuelve un diccionario con todos los usuarios existentes
        en la base de datos en orden de mas rareza a menos rareza
        """
        generador = self._get_lista_usuarios().get_users_as_dict()
        resultado: Custom_types.Ranking.JSONRanking = {"usuarios": []}

        for indice, diccionario_actual in enumerate(generador):
            # El bucle termina cuando el iterador no apunta a nada
            diccionario_actual["puesto"] = indice+1
            resultado["usuarios"].append(diccionario_actual)

        return resultado

    def _get_lista_usuarios(self) -> ListaUsuarios:
        """
        pre:
        post: Devuelve un objeto ListaUsuarios, que colecciona
        UsuariosRanking
        """
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
        resultado = ListaUsuarios()
        """
        He cambiado esto, para que en caso de que no sea capaz de
        obtener los usuarios de la BD, que no explote y de 
        Internal Server Error - Liviu (15:28 - 11/01/2026)
        """

        if len(resultado_sql) > 0:
            """
            Si existe algun resultado en la consulta. En el diagrama de secuencia/comunicacion
            es un unico next(), no en un bucle.
            """
            resultado = ListaUsuarios()

            usuario_actual: UsuarioRanking = UsuarioRanking("", 0) # Un UsuarioRanking vacio

            for fila in resultado_sql:

                if not usuario_actual.es_mi_nombre(fila["NombreUsuario"]):
                    if not usuario_actual.es_mi_nombre(""):
                        """
                        En el caso de que sea el UsuarioRanking vacio del principio,
                        porque ese usuario no existe en la BD.
                        """
                        resultado.insercion_ordenada(usuario_actual)

                    usuario_actual = UsuarioRanking(fila["NombreUsuario"], 0)

                usuario_actual.add_rareza(int(fila["Rareza"]))

            resultado.insercion_ordenada(usuario_actual)
            """
            Cuando termina el ciclo, hay que ainadir el ultimo usuario ranking,
            porque este ultimo nunca cumple con las condiciones dentro del ciclo.
            """

        return resultado

    def _get_puesto_by_nombre(self, nombre: str) -> int:
        """
        pre: el usuario se encuentra en la base de datos
        post: devuelve el puesto del usuario
        """
        lista_actual: ListaUsuarios = self._get_lista_usuarios()
        return ( lista_actual.get_index(nombre) + 1)

    def mostrarUsuario(self, pNombreUsuario: str, pNombreAmigo: str) -> Custom_types.Ranking.JSONRankingUsuario:
        """
        pre: "pNombreUsuario" no esta vacio
        post: Dado un nombre de usuario, devuelve un diccionario con
        su nombre, una lista de pokemon que usa y sus nombres no comunes
        correspondientes.
        """
        resultado: Custom_types.Ranking.JSONRankingUsuario = None
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

        resultado_sql: List[sqlite3.Row] = self.bd.select(sentence, (pNombreAmigo,))

        if len(resultado_sql) > 0:
            """
            Si existe algun resultado en la consulta. En el diagrama de secuencia/comunicacion
            es un unico next(), no en un bucle.
            """
            puesto_actual: int = self._get_puesto_by_nombre(pNombreAmigo)
            resultado = {"nombre": pNombreAmigo,
                         "equipoEspecie": [],
                         "equipoCustom": [],
                         "fotoPokemon": [],
                         "puesto": puesto_actual,
                         "estado_amigo": Custom_types.PerfilUsuario.NO_AMIGO
                         }

            for fila in resultado_sql:
                nombre_especie: str = fila["NombreEspecie"]
                resultado["equipoEspecie"].append(nombre_especie)
                resultado["equipoCustom"].append(fila["NombreCustom"])
                sprite_actual = json.loads(PokeDex.get_instance().getInfo(nombre_especie))
                if not "error" in sprite_actual.keys():
                    # TODO: La linea sprite actual hay que cambiarla a una llamada de la Pokedex
                    resultado["fotoPokemon"].append(sprite_actual["imagen"])

            if pNombreUsuario == pNombreAmigo:
                """
                Comprobamos si la persona que ha iniciado sesion, ha ido
                a ver su perfil desde el ranking.
                """
                resultado["estado_amigo"] = Custom_types.PerfilUsuario.TU_MISMO
            else:
                sentence = """
                    SELECT *
                    FROM AmigoDe
                    INNER JOIN Usuario
                    ON Usuario.NombreUsuario = AmigoDe.NombreUsuario1
                    WHERE ( Usuario.NombreUsuario = ? AND AmigoDe.NombreUsuario2 = ? );
                """

                resultado_sql: List[sqlite3.Row] = self.bd.select(sentence, (pNombreUsuario,pNombreAmigo,))

                if len(resultado_sql) > 0:
                    """
                    Si existe algun resultado en la consulta. En el diagrama de secuencia/comunicacion
                    es un unico next(), no en un bucle.
                    """
                    resultado["estado_amigo"] = Custom_types.PerfilUsuario.SI_AMIGO

        return resultado