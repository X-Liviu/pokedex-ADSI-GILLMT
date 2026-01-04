import sqlite3
from app.controller.model.gestorCopiasEquipo_controller import gestorCopiasEquipo
from app.model.usuario import Usuario


class gestorUsuario:
    _instancias_usuarios = {}
    def __init__(self, db, usuario) :
        self.db = db
        self.usuario = usuario
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
            #     pokemon_id=1,
            #     nombre_custom="Pika-Tata",
            #     especie="Pikachu",
            #     imagen="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
            #     db=db)
            #
            # p2 = Pokemon(
            #     pokemon_id=2,
            #     nombre_custom="Repollito",
            #     especie="Bulbasaur",
            #     imagen="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
            #     db=db
            # )
            #
            # # 2. Creamos un equipo y le metemos esos Pokémon
            # equipo_test = Equipo(numEquipo=1, db=db)
            # equipo_test.lista_pokemon = [p1, p2]
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
            #     lista_equipos=[equipo_test],  # Le pasamos el equipo con los 2 pokémon
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
            # 1. Guardamos el Equipo
            self.db.insert(
                sentence="INSERT INTO Equipo (idEquipo, NombreUsuario) VALUES (?,?)",
                parameters=(numEquipo, self.usuario.nombre_usuario)
            )

            # 2. Guardamos cada Pokémon del equipo
            for pokemon in equipo.lista_pokemon:  # Usamos la lista del equipo encontrado
                info = pokemon.getInfo()  # Esto devuelve un diccionario

                # Usamos las llaves del diccionario para los parámetros
                self.db.insert(
                    sentence="""INSERT INTO Pokemon
                                (idPokemon, NombreCustom, Rareza, Shiny, Altura, Peso, NombreEspecie, Imagen)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    parameters=(
                        info["pokemon id"],
                        info["nombre_custom"],
                        info["rareza"],
                        1 if info["shiny"] else 0,  # Convertimos True/False a 1/0 para SQL
                        info["altura"],
                        info["peso"],
                        info["especie"],
                        info["imagen"]
                    )
                )

                # 3. Relacionamos el Pokémon con el Equipo
                self.db.insert(
                    sentence="INSERT INTO PokemonEnEquipo (idEquipo, idPokemon) VALUES (?,?)",
                    parameters=(numEquipo, info["pokemon id"])
                )

    def tieneEquipos(self) :
        return self.usuario.tieneEquipos()

    def getListaEquipos(self) :
        return self.usuario.getListaEquipos()

    def mostrarInfoEquipo(self, numEquipo) :
        equipo = self.usuario.buscarEquipo(numEquipo)
        return equipo.mostrarInfoEquipo()

    def clonarEquipo(self, numEquipo) :
        gestorCopiasEquipo.clonarEquipo(self.usuario, numEquipo)

    def borrarEquipo(self, numEquipo) :
        return self.usuario.borrarEquipo(numEquipo)

    def borrarPokemon(self, numEquipo, idPokemon):
        equipo = self.usuario.buscarEquipo(numEquipo)
        if equipo:
            equipo.borrarPokemon(idPokemon)

    def compararCopias(self,numEquipo) :
        gestorCopiasEquipo.compararCopiasEliminar(self.usuario, numEquipo)
        gestorCopiasEquipo.compararCopiasAniadir(self.usuario, numEquipo)
        gestorCopiasEquipo.finalizarEdicion(self.usuario.nombre_usuario)

    def descartarCambios(self, numEquipo) :
        gestorCopiasEquipo.descartarCambios(self.usuario, numEquipo)

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
             VALUES ( {self.usuario.getName()}, {nombreUsuario} );
            """

            try:
                self.db.insert(comandosSQL)
            except sqlite3.Error:
                resultado = not resultado

        return resultado