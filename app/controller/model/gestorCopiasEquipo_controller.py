class gestorCopiasEquipo:

    def __init__(self) -> None:
        # Diccionario para separar las copias por usuario
        self._almacen_copias = {}

    def clonarEquipo(self, usuario, numEquipo):
        equipoOriginal = usuario.buscarEquipo(numEquipo)
        if equipoOriginal:
            # Usamos el nombre del usuario como clave
            self._almacen_copias[usuario.nombre_usuario] = equipoOriginal.clonar()

    def obtener_copia(self, nombre_usuario):
        return self._almacen_copias.get(nombre_usuario)

    def compararCopiasEliminar(self, usuario, numEquipo,db):
        equipoEditado = usuario.buscarEquipo(numEquipo)
        copia = self.obtener_copia(usuario.nombre_usuario)

        if equipoEditado and copia:
            for pokemon in copia.lista_pokemon:
                # Si el pokemon estaba en la copia pero NO en el editado, se borra
                if not equipoEditado.buscarPokemon(pokemon.pokemon_id):
                    # 1. Obtenemos el ID único de la base de datos (idPokemon)
                    res = db.select("SELECT idPokemon FROM Pokemon WHERE numPokemon = ? AND NombreCustom = ?",
                                    (pokemon.pokemon_id, pokemon.nombre_custom))

                    if res:
                        id_pokemon_bd = res[0][0]

                        # 2. Borramos la relación en el equipo específico
                        # (Añadir idEquipoInterno sería lo ideal para estar 100% seguros)
                        db.delete(
                            sentence="DELETE FROM PokemonEnEquipo WHERE idPokemon = ?",
                            parameters=(id_pokemon_bd,)  # <--- Coma añadida
                        )

                        # 3. Borramos el Pokémon de la tabla general
                        db.delete(
                            sentence="DELETE FROM Pokemon WHERE idPokemon = ?",
                            # Usamos el ID de la BD, no el numPokemon
                            parameters=(id_pokemon_bd,)  # <--- Coma añadida
                        )
                    else:
                        print(f"Aviso: No se encontró el pokemon {pokemon.nombre_custom} en la base de datos.")

    def compararCopiasAniadir(self, usuario, numEquipo,db):
        equipoEditado = usuario.buscarEquipo(numEquipo)
        copia = self.obtener_copia(usuario.nombre_usuario)

        if equipoEditado and copia:
            for pokemon in equipoEditado.lista_pokemon:
                # Si el pokemon es nuevo (no estaba en la copia), se guarda
                if not copia.buscarPokemon(pokemon.pokemon_id):
                    info = pokemon.getInfo()
                    id_poki_real = db.insert(
                        sentence="""INSERT INTO Pokemon
                                        (numPokemon, NombreCustom, Rareza, Shiny, Altura, Peso, NombreEspecie, Imagen)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        parameters=(info["pokemon_id"], info["nombre_custom"], info["rareza"], 1 if info["shiny"] else 0,
                                    info["altura"], info["peso"], info["especie"], info["imagen"])
                    )

                    # 2. Obtenemos el ID de la tabla Equipo para este usuario
                    res = db.select("SELECT idEquipo FROM Equipo WHERE numEquipo = ? AND NombreUsuario = ?",
                                    (numEquipo, usuario.nombre_usuario))

                    if res:
                        id_equipo_bd = res[0][0]
                        # 3. Creamos la relación
                        db.insert(
                            sentence="INSERT INTO PokemonEnEquipo (idEquipoInterno, idPokemon) VALUES (?,?)",
                            parameters=(id_equipo_bd, id_poki_real)
                        )

    def descartarCambios(self, usuario, numEquipo):
        equipo_sucio = usuario.buscarEquipo(numEquipo)
        copia = self.obtener_copia(usuario.nombre_usuario)

        if equipo_sucio and copia:
            equipo_sucio.restaurarEquipo(copia)
            # Limpiamos la RAM después de restaurar
            self.finalizarEdicion(usuario.nombre_usuario)

    def finalizarEdicion(self, nombre_usuario):
        if nombre_usuario in self._almacen_copias:
            del self._almacen_copias[nombre_usuario]

# Instancia global del gestor
gestor_copias = gestorCopiasEquipo()