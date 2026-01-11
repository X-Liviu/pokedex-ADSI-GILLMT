import sqlite3
from app.controller.model.gestorCopiasEquipo_controller import gestorCopiasEquipo
from app.model.usuario import Usuario


class gestorUsuario:
    _instancias_usuarios = {}

    def __init__(self, db, usuario):
        self.db = db
        self.usuario = usuario
        self.g_copias = gestorCopiasEquipo()

    @classmethod
    def iniciarSesion(cls, pNomUsuario: str, pContrasena: str, db) -> bool:
        # 1. Consultamos a la base de datos
        sql = "SELECT * FROM Usuario WHERE NombreUsuario = ? AND Contrasena = ?"
        resultado = db.select(sql, (pNomUsuario, pContrasena))

        if resultado and len(resultado) > 0:
            fila = resultado[0]

            # 2. Creamos el objeto Usuario
            usuario_obj = Usuario(
                nombre=fila['Nombre'],
                apellido=fila['Apellido'],
                nombre_usuario=fila['NombreUsuario'],
                correo=fila['Correo'],
                contrasena=fila['Contrasena'],
                rol=fila['Rol'],
                lista_equipos=[],  # Se cargará vacía de momento
                db=db
            )

            # 3. Guardamos la instancia en el diccionario (Cache)
            cls._instancias_usuarios[pNomUsuario] = cls(db, usuario_obj)
            return True

        return False

    @classmethod
    def getMyGestorUsuario(cls, nombre_usuario, db):
        # Si el usuario no está en memoria (por ejemplo, tras reiniciar servidor), lo recuperamos de la BD
        if nombre_usuario not in cls._instancias_usuarios:

            # --- AQUÍ ESTABA EL ERROR (db.getUsuario no existe) ---
            # CORRECCIÓN: Hacemos el SELECT manualmente:
            sql = "SELECT * FROM Usuario WHERE NombreUsuario = ?"
            resultado = db.select(sql, (nombre_usuario,))

            if resultado and len(resultado) > 0:
                fila = resultado[0]
                usuario = Usuario(
                    nombre=fila['Nombre'],
                    apellido=fila['Apellido'],
                    nombre_usuario=fila['NombreUsuario'],
                    correo=fila['Correo'],
                    contrasena=fila['Contrasena'],
                    rol=fila['Rol'],
                    lista_equipos=[],  # TODO: Aquí se deberían cargar los equipos existentes si fuera necesario
                    db=db
                )
                cls._instancias_usuarios[nombre_usuario] = cls(db, usuario)
            else:
                return None  # Usuario no encontrado en BD

        return cls._instancias_usuarios.get(nombre_usuario)

    def crearEquipo(self):
        return self.usuario.addEquipo()

    def aniadirPokemon(self, nombreEspecie, nombrePokemon, numEquipo):
        equipo = self.usuario.buscarEquipo(numEquipo)
        if equipo and not equipo.tiene6():
            return equipo.addPokemon(nombreEspecie, nombrePokemon)
        else:
            return -1

    def guardarEquipo(self, numEquipo):
        equipo = self.usuario.buscarEquipo(numEquipo)
        if equipo:
            # 1. Guardamos el Equipo
            try:
                id_bd_real = self.db.insert(
                    sentence="INSERT INTO Equipo (numEquipo, NombreUsuario) VALUES (?,?)",
                    parameters=(numEquipo, self.usuario.nombre_usuario)
                )

                for pokemon in equipo.lista_pokemon:
                    info = pokemon.getInfo()

                    # 2. Guardamos el Pokémon
                    id_poki_real = self.db.insert(
                        sentence="""INSERT INTO Pokemon
                                    (numPokemon, NombreCustom, Rareza, Shiny, Altura, Peso, NombreEspecie, Imagen)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        parameters=(info["pokemon_id"], info["nombre_custom"], info["rareza"],
                                    1 if info["shiny"] else 0,
                                    info["altura"], info["peso"], info["especie"], info["imagen"])
                    )

                    # 3. Relación Pokemon - Equipo
                    self.db.insert(
                        sentence="INSERT INTO PokemonEnEquipo (idEquipoInterno, idPokemon) VALUES (?,?)",
                        parameters=(id_bd_real, id_poki_real)
                    )
            except sqlite3.Error as e:
                print(f"Error guardando equipo: {e}")

    def tieneEquipos(self):
        return self.usuario.tieneEquipos()

    def getListaEquipos(self):
        return self.usuario.getListaEquipos()

    def mostrarInfoEquipo(self, numEquipo):
        equipo = self.usuario.buscarEquipo(numEquipo)
        if equipo:
            return equipo.mostrarInfoEquipo()
        return None

    def clonarEquipo(self, numEquipo):
        self.g_copias.clonarEquipo(self.usuario, numEquipo)

    def borrarEquipo(self, numEquipo):
        equipo = self.usuario.buscarEquipo(numEquipo)
        if equipo:
            self.usuario.lista_equipos.remove(equipo)
            return True
        return False

    def borrarPokemon(self, numEquipo, idPokemon):
        equipo = self.usuario.buscarEquipo(numEquipo)
        if equipo:
            equipo.borrarPokemon(idPokemon)

    def compararCopias(self, numEquipo):
        self.g_copias.compararCopiasEliminar(self.usuario, numEquipo, self.db)
        self.g_copias.compararCopiasAniadir(self.usuario, numEquipo, self.db)
        self.g_copias.finalizarEdicion(self.usuario.nombre_usuario)

    def descartarCambios(self, numEquipo):
        self.g_copias.descartarCambios(self.usuario, numEquipo)

    def mejorPokemon(self, numEquipo):
        return self.usuario.mejorPokemon(numEquipo)

    def aniadirAmigo(self, nombreUsuario: str) -> bool:
        resultado: bool = self.usuario.ainadirAmigo(nombreUsuario)
        if resultado:
            comandosSQL: str = "INSERT INTO AmigoDe (NombreUsuario1, NombreUsuario2) VALUES (?, ?);"
            try:
                self.db.insert(comandosSQL, (self.usuario.nombre_usuario, nombreUsuario))
            except sqlite3.Error:
                resultado = False
        return resultado

    def tieneAmigos(self) -> bool:
        return self.usuario.tieneAmigos()