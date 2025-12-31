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

    def compararCopiasEliminar(self, usuario, numEquipo):
        equipoEditado = usuario.buscarEquipo(numEquipo)
        copia = self.obtener_copia(usuario.nombre_usuario)

        if equipoEditado and copia:
            for pokemon in copia.lista_pokemon:
                # Si el pokemon estaba en la copia pero NO en el editado, se borra
                if not equipoEditado.buscarPokemon(pokemon.pokemon_id):
                    pokemon.borrarPokemonBD()

    def compararCopiasAniadir(self, usuario, numEquipo):
        equipoEditado = usuario.buscarEquipo(numEquipo)
        copia = self.obtener_copia(usuario.nombre_usuario)

        if equipoEditado and copia:
            for pokemon in equipoEditado.lista_pokemon:
                # Si el pokemon es nuevo (no estaba en la copia), se guarda
                if not copia.buscarPokemon(pokemon.pokemon_id):
                    pokemon.guardarPokemon()

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