import sqlite3
from app.controller.model.gestorCopiasEquipo_controller import gestorCopiasEquipo
from app.model.usuario import Usuario


class gestorUsuario:
    _instancias_usuarios = {}
    def __init__(self, db, usuario) :
        self.db = db
        self.usuario = usuario
        self.g_copias = gestorCopiasEquipo()
        pass

    @classmethod
    def getMyGestorUsuario(cls, nombre_usuario, db):
        if nombre_usuario not in cls._instancias_usuarios:
            # 1. Creamos el objeto Usuario completo primero
            usuario = db.getUsuario(nombre_usuario)

            # #PRUEBAS TATA
            # from app.model.pokemon import Pokemon
            # from app.model.equipo import Equipo
            # # 1. Creamos un par de Pokémon de prueba
            # p1 = Pokemon(
            #     pokemon_id=11,
            #     nombre_custom="Pika-Tata",
            #     especie="Pikachu",
            #     imagen="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
            # )
            #
            # p2 = Pokemon(
            #     pokemon_id=12,
            #     nombre_custom="Repollito",
            #     especie="Bulbasaur",
            #     imagen="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"
            # )
            #
            # p3 = Pokemon(
            #     pokemon_id=21,
            #     nombre_custom="tataCerdo",
            #     shiny=True,
            #     especie="Spearow",
            #     imagen="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/21.png"
            # )
            #
            # # 2. Creamos un equipo y le metemos esos Pokémon
            # equipo_test = Equipo(numEquipo=1)
            # equipo_test.lista_pokemon = [p1, p2]
            # equipo_test2 = Equipo(numEquipo=2)
            # equipo_test2.lista_pokemon = [p1, p3]
            #
            # # 3. Creamos el objeto Usuario con los datos de prueba
            # # (Asegúrate de que el orden de los argumentos sea el de tu clase Usuario)
            # usuario = Usuario(
            #     nombre="Tata",
            #     apellido="Batata",
            #     nombre_usuario=nombre_usuario,
            #     correo="tata@pokedex.com",
            #     contrasena="1234",
            #     rol="usuario",
            #     lista_equipos=[equipo_test,equipo_test2],  # Le pasamos el equipo con los 2 pokémon
            #     db=db
            # )
            # 2. Creamos el gestor pasándole el objeto completo
            cls._instancias_usuarios[nombre_usuario] = cls(db, usuario)

        return cls._instancias_usuarios[nombre_usuario]

    def crearEquipo(self) :
        return self.usuario.addEquipo()

    def aniadirPokemon(self, nombreEspecie, nombrePokemon, numEquipo):
        equipo = self.usuario.buscarEquipo(numEquipo)
        if not equipo.tiene6():
            return equipo.addPokemon(nombreEspecie, nombrePokemon)
        else:
            return -1

    def guardarEquipo(self, numEquipo):
        equipo = self.usuario.buscarEquipo(numEquipo)
        if equipo:
            # 1. Guardamos el Equipo. Pasamos TU numEquipo (1 o 2) y el usuario.
            # SQLite generará un idInterno único automáticamente (ej: 45)
            id_bd_real = self.db.insert(
                sentence="INSERT INTO Equipo (numEquipo, NombreUsuario) VALUES (?,?)",
                parameters=(numEquipo, self.usuario.nombre_usuario)
            )

            for pokemon in equipo.lista_pokemon:
                info = pokemon.getInfo()

                # 2. Guardamos el Pokémon y obtenemos su ID único
                id_poki_real = self.db.insert(
                    sentence="""INSERT INTO Pokemon
                                    (numPokemon, NombreCustom, Rareza, Shiny, Altura, Peso, NombreEspecie, Imagen)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    parameters=(info["pokemon_id"],info["nombre_custom"], info["rareza"], 1 if info["shiny"] else 0,
                                info["altura"], info["peso"], info["especie"], info["imagen"])
                )

                # 3. RELACIÓN: Usamos los IDs reales que nos ha dado la base de datos
                self.db.insert(
                    sentence="INSERT INTO PokemonEnEquipo (idEquipoInterno, idPokemon) VALUES (?,?)",
                    parameters=(id_bd_real, id_poki_real)
                )

    def tieneEquipos(self) :
        return self.usuario.tieneEquipos()

    def getListaEquipos(self) :
        return self.usuario.getListaEquipos()

    def mostrarInfoEquipo(self, numEquipo) :
        equipo = self.usuario.buscarEquipo(numEquipo)
        return equipo.mostrarInfoEquipo()

    def clonarEquipo(self, numEquipo) :
        self.g_copias.clonarEquipo(self.usuario, numEquipo)

    def borrarEquipo(self, numEquipo) :
        equipo = self.usuario.buscarEquipo(numEquipo)
        if equipo:
            self.usuario.lista_equipos.remove(equipo)
            return True
        return False

    def borrarPokemon(self, numEquipo, idPokemon):
        equipo = self.usuario.buscarEquipo(numEquipo)
        if equipo:
            equipo.borrarPokemon(idPokemon)

    def compararCopias(self,numEquipo) :
        self.g_copias.compararCopiasEliminar(self.usuario, numEquipo, self.db)
        self.g_copias.compararCopiasAniadir(self.usuario, numEquipo, self.db)
        self.g_copias.finalizarEdicion(self.usuario.nombre_usuario)

    def descartarCambios(self, numEquipo) :
        self.g_copias.descartarCambios(self.usuario, numEquipo)

    def mejorPokemon(self, numEquipo) :
        return self.usuario.mejorPokemon(numEquipo)

    # Marco lo usa en el Ranking, pero pertence a esta clase
    def aniadirAmigo(self, nombreUsuario: str) -> bool:
        """
        pre: Se da por hecho que "nombreUsuario" no esta vacio
        post: Ainade al usuario que se encuentra como atributo y
        el que esta como parametro en sus listas de amigos. Si
        salio bien, devuelve True y en caso contrario False.
        """
        resultado: bool = self.usuario.ainadirAmigo(nombreUsuario)

        if resultado:
            comandosSQL: str = f"""
                         INSERT INTO Amigo_de (NombreUsuario1, NombreUsuario2)
                         VALUES (?, ?);
            """

            try:
                self.db.insert(comandosSQL, self.usuario.getName(), nombreUsuario)
            except sqlite3.Error:
                resultado = not resultado

        return resultado