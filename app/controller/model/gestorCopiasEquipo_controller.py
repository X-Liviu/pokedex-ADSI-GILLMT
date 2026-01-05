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
                    db.delete(
                        sentence="DELETE FROM PokemonEnEquipo WHERE idPokemon = ?",
                        parameters=(pokemon.pokemon_id,)
                    )
                    db.delete(
                        sentence="DELETE FROM Pokemon WHERE idPokemon = ?",
                        parameters=(pokemon.pokemon_id,)
                    )

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
                                        (NombreCustom, Rareza, Shiny, Altura, Peso, NombreEspecie, Imagen)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        parameters=(info["nombre_custom"], info["rareza"], 1 if info["shiny"] else 0,
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