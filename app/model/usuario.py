from app.model.equipo import Equipo

class Usuario:
    def __init__(self, nombre: str, apellido: str, nombre_usuario: str,
                 correo: str, contrasena: str, rol: str, lista_equipos: list, db):
        self.nombre = nombre
        self.apellido = apellido
        self.nombre_usuario = nombre_usuario
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol
        self.lista_equipos = lista_equipos
        self.db = db
        # self.amigos = []

    def addEquipo(self) :
        if self.tieneEquipos() :
            ultimo_num = max(equipo.numEquipo for equipo in self.lista_equipos)
            numEquipo = ultimo_num + 1
        else:
            numEquipo = 1

        nuevo_equipo = Equipo(numEquipo)
        self.lista_equipos.append(nuevo_equipo)
        return nuevo_equipo.numEquipo

    def buscarEquipo(self, numEquipo: int):
        for equipo in self.lista_equipos:
            if equipo.esEsteEquipo(numEquipo):
                return equipo
        return None

    def tieneEquipos(self):
        if self.lista_equipos:
            return True
        else:
            return False

    def getListaEquipos(self):
        equipos_info = []

        # Recorremos la lista de objetos Equipo que tiene el usuario
        for equipo in self.lista_equipos:
            # Buscamos la imagen del primer pokemon (la portada)
            # Usamos un "placeholder" si el equipo está vacío
            imagen_portada = "sin_imagen.png"
            if len(equipo.lista_pokemon) > 0:
                imagen_portada = equipo.lista_pokemon[0].imagen

            # Creamos un pequeño diccionario por cada equipo
            info_equipo = {
                "numEquipo": equipo.numEquipo,
                "foto_principal": imagen_portada,
                "cantidad_pokemon": len(equipo.lista_pokemon)
            }
            equipos_info.append(info_equipo)

        # Estructura final del JSON
        datos = {
            "usuario": self.nombre_usuario,
            "total_equipos": len(self.lista_equipos),
            "equipos": equipos_info
        }

        return datos
        # Convertimos a cadena JSON con sangría para que sea legible
        #return json.dumps(datos, indent=4)

    def mejorPokemon(self, numEquipo):
        elEquipo = self.buscarEquipo(numEquipo)
        if elEquipo != None :
            return elEquipo.getMejorPokemon()
        else:
            return -1

    def ainadirAmigo(self, nombre):
        resultado = False
        if not self._esAmigo(nombre):
            pass
            # nuevoAmigo = Usuario()
            # self.lista_amigos.append(nuevoAmigo)
            # resultado = not resultado
        return resultado

    """
    def _esAmigo(self, nombre):
        resultado = False
        indice = 0
        longitud = len(self.amigos)
        while not resultado and indice < longitud:
            if self.amigos[indice].esNombre(nombre):
                resultado = not resultado
            else:
                indice += 1
        return resultado
    """