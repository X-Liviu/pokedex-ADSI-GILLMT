import sqlite3
import random
from app.controller.model.gestorCopiasEquipo_controller import gestorCopiasEquipo
from app.model.usuario import Usuario


class gestorUsuario:
    _instancias_usuarios = {}
    _cambios_pendientes = {}

    listaUsuariosParaAdmin = []

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
            sql = """
                  SELECT NombreUsuario1 \
                  FROM AmigoDe \
                  WHERE NombreUsuario2 = ?
                  UNION
                  SELECT NombreUsuario2 \
                  FROM AmigoDe \
                  WHERE NombreUsuario1 = ? \
                  """
            resultado = db.select(sql, (pNomUsuario, pNomUsuario))

            # 2. Creamos el objeto Usuario
            usuario_obj = Usuario(
                nombre=fila['Nombre'],
                apellido=fila['Apellido'],
                nombre_usuario=fila['NombreUsuario'],
                correo=fila['Correo'],
                contrasena=fila['Contrasena'],
                rol=fila['Rol'],
                lista_equipos=[],  # Se cargará vacía de momento
                db=db,
                amigos = resultado
            )

            # 3. Guardamos la instancia en el diccionario (Cache)
            cls._instancias_usuarios[pNomUsuario] = cls(db, usuario_obj)
            return True

        return False

    # Dentro de la clase gestorUsuario

    @classmethod
    def cargarUsuario(cls, nombre_usuario, db):

        sql = "SELECT * FROM Usuario WHERE NombreUsuario = ?"
        resultado = db.select(sql, (nombre_usuario,))

        if resultado and len(resultado) > 0:
            fila = resultado[0]
            sql = """
                  SELECT NombreUsuario1 \
                  FROM AmigoDe \
                  WHERE NombreUsuario2 = ?
                  UNION
                  SELECT NombreUsuario2 \
                  FROM AmigoDe \
                  WHERE NombreUsuario1 = ? \
                  """
            resultado = db.select(sql, (nombre_usuario, nombre_usuario))
                # 3. Reconstruimos el objeto Usuario (igual que en iniciarSesion)
            usuario_obj = Usuario(
                nombre=fila['Nombre'],
                apellido=fila['Apellido'],
                nombre_usuario=fila['NombreUsuario'],
                correo=fila['Correo'],
                contrasena=fila['Contrasena'],
                rol=fila['Rol'],
                lista_equipos=[],  # O cargar equipos si es necesario
                db=db,
                amigos = resultado
            )

            # 4. Creamos el gestor y lo guardamos en el diccionario
            nuevo_gestor = cls(db, usuario_obj)
            cls._instancias_usuarios[nombre_usuario] = nuevo_gestor
        return None

    @classmethod
    def getMyGestorUsuario(cls, nombre_usuario, db=None):
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

    @classmethod
    def registrarUsuario(cls, pNom: str, pAp: str, pCorreo: str, pNomUsuario: str, pContrasena: str, pContrasenaRep: str, db) -> int:

        # CASO 1: Contraseñas no coinciden
        if pContrasena != pContrasenaRep:
            return -1

        # CASO 2: Usuario o correo ya existen
        sql_check = "SELECT NombreUsuario FROM Usuario WHERE NombreUsuario = ? OR Correo = ?"
        filas = db.select(sql_check, (pNomUsuario, pCorreo))

        if len(filas) > 0:
            return -2

        # CASO 3: Registro Correcto (verificado o no verificado es aleatorio, ya que realmente no influye en nada, solo para que pueda ser probado el caso de uso de ver lista usuarios.
        rol_asignado = 'NOVERIF' if random.random() < 0.20 else 'VERIF'

        sql_insert = """
                     INSERT INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol)
                     VALUES (?, ?, ?, ?, ?, ?) \
                     """
        try:
            # Pasamos 'rol_asignado' en la consulta
            db.insert(sql_insert, (pNomUsuario, pNom, pAp, pCorreo, pContrasena, rol_asignado))
            return 0  # Éxito

        except Exception as e:
            print(f"Error en BD: {e}")
            return -2

    def verificarCambios(self, pNomUsuario: str, pUsuarioNuevo: str, pContraNueva: str) -> bool:
        if pUsuarioNuevo and len(pUsuarioNuevo.strip()) > 0:
            if pNomUsuario != pUsuarioNuevo:
                return True

        if pContraNueva and len(pContraNueva) > 0:
            return True
        return False

    def guardarModificacionTemporal(self, pNomUsuario: str, pNom: str, pAp: str, pCorreo: str, pUsuarioNuevo: str, pNuevaContra: str):
        # Guardamos en el diccionario estático (simulando memoria del servidor)
        datos = {
            "nombre": pNom,
            "apellido": pAp,
            "correo": pCorreo,
            "usuario": pUsuarioNuevo,
            "contrasena": pNuevaContra
        }
        gestorUsuario._cambios_pendientes[pNomUsuario] = datos

    def recuperarModificacionTemporal(self, pNomUsuario: str) -> Usuario:
        # Recuperamos el diccionario
        datos = gestorUsuario._cambios_pendientes.get(pNomUsuario)
        if not datos:
            return None

        return Usuario(datos['nombre'], datos['apellido'], datos['usuario'],
                       datos['correo'], datos['contrasena'], 'VERIF', [], None) #TODO revisar lo del rol por defecto de ahora

    def modificarUsuarioEnMemoriaYBD(self, pNom: str, pAp: str, pCorreo: str, pUsuarioNuevo: str, pNuevaContra: str):
        # --- LÓGICA DE MEZCLA INTELIGENTE ---
        # Si el input viene vacío, cogemos el dato que ya tiene el usuario.
        final_nom = pNom if pNom and pNom.strip() else self.usuario.getNombre()
        final_ap = pAp if pAp and pAp.strip() else self.usuario.getApellido()
        final_correo = pCorreo if pCorreo and pCorreo.strip() else self.usuario.getCorreo()
        final_usuario = pUsuarioNuevo if pUsuarioNuevo and pUsuarioNuevo.strip() else self.usuario.getNomUsuario()
        final_contra = pNuevaContra if pNuevaContra and pNuevaContra.strip() else self.usuario.getContrasena()

        # Guardamos el nombre viejo para el WHERE antes de que el objeto cambie
        # Esto es vital para que la SQL encuentre la fila original
        nombre_viejo_where = self.usuario.getNomUsuario()

        # 1. Modificar en memoria (usando los valores finales)
        self.usuario.modificarDatos(final_nom, final_ap, final_correo, final_usuario, final_contra)

        # 2. Modificar en BD (Llamada SQL)
        sql = """
              UPDATE Usuario
              SET Nombre=?, \
                  Apellido=?, \
                  Correo=?, \
                  NombreUsuario=?, \
                  Contrasena=?
              WHERE NombreUsuario = ? \
              """

        # Ejecutamos el SQL con los datos finales y el nombre viejo para el WHERE
        self.db.update(sql, (final_nom, final_ap, final_correo, final_usuario, final_contra, nombre_viejo_where))

        # Actualizar caché si cambió el nombre de usuario
        if nombre_viejo_where != final_usuario:
            if nombre_viejo_where in gestorUsuario._instancias_usuarios:
                del gestorUsuario._instancias_usuarios[nombre_viejo_where]
            gestorUsuario._instancias_usuarios[final_usuario] = self

    def validarCredencialesYGuardarCambios(self, pNomUsuario: str, pContrasena: str) -> str:
        """
        Paso 10b: validarCredencialesYGuardarCambios(...) : String
        Retorna:
            - str: El nombre de usuario definitivo (nuevo o viejo) si todo salió bien.
            - None: Si la contraseña era incorrecta o hubo un error.
        """
        # Paso 11b: validarPassword
        if not self.usuario.validarPassword(pContrasena):
            return None  # Equivale a False (contraseña incorrecta)

        # Paso 12ba: recuperarModificacionTemporal
        datosUsuarioModif = self.recuperarModificacionTemporal(pNomUsuario)
        if not datosUsuarioModif:
            return None # Error interno: no había datos temporales

        # Paso 13ba (Lógica): Deconstrucción
        elNombre = datosUsuarioModif.getNombre()
        elAp = datosUsuarioModif.getApellido()
        elCorreo = datosUsuarioModif.getCorreo()
        elNomUsuario = datosUsuarioModif.getNomUsuario()
        laContra = datosUsuarioModif.getContrasena()

        # Ejecución de la modificación persistente
        self.modificarUsuarioEnMemoriaYBD(elNombre, elAp, elCorreo, elNomUsuario, laContra)

        # Limpieza
        if pNomUsuario in gestorUsuario._cambios_pendientes:
            del gestorUsuario._cambios_pendientes[pNomUsuario]

        return self.usuario.getNomUsuario()

    @classmethod
    def obtenerUsuariosParaAdmin(cls, db):
        """
        Flujo: SELECT -> Crear Objetos Usuario -> Guardar en listaUsuariosParaAdmin -> Devolver Diccionarios
        """
        cls.listaUsuariosParaAdmin = []  # Limpiamos la lista anterior
        lista_diccionarios = []

        sql = "SELECT Nombre, Apellido, NombreUsuario, Correo, Contrasena, Rol FROM Usuario WHERE Rol = 'NOVERIF'"

        resultado = db.select(sql, ())

        for fila in resultado:
            # 1. Crear objeto Usuario
            nuevo_usuario = Usuario(
                nombre=fila['Nombre'],
                apellido=fila['Apellido'],
                nombre_usuario=fila['NombreUsuario'],
                correo=fila['Correo'],
                contrasena=fila['Contrasena'],
                rol=fila['Rol'],
                lista_equipos=[],
                db=db
            )

            # 2. Añadir a la lista en memoria
            cls.listaUsuariosParaAdmin.append(nuevo_usuario)

            # 3. Preparar diccionario para la vista
            lista_diccionarios.append({
                "nombre": fila['Nombre'],
                "apellido": fila['Apellido'],
                "nomUsuario": fila['NombreUsuario'],
                "rol": fila['Rol']
            })

        return lista_diccionarios

    @classmethod
    def buscarUsuarioDeLaListaParaAdmin(cls, pNomUsuario: str):
        """
        Busca un usuario por su nombre de usuario dentro de la lista estática cargada en memoria.
        Retorna el objeto Usuario o None.
        """
        for usuario in cls.listaUsuariosParaAdmin:
            if usuario.getNomUsuario() == pNomUsuario:
                return usuario
        return None

    @classmethod
    def aprobarUsuario(cls, pNomUsuario: str, db) -> bool:
        """
        Actualiza a VERIF en BD.
        """
        try:
            sql = "UPDATE Usuario SET Rol='VERIF' WHERE NombreUsuario = ?"
            db.update(sql, (pNomUsuario,))

            # Verificación opcional (Paso 16-19 del flujo)
            sql_check = "SELECT Rol FROM Usuario WHERE NombreUsuario = ?"
            res = db.select(sql_check, (pNomUsuario,))
            if res and res[0]['Rol'] == 'VERIF':
                return True
            return False
        except Exception as e:
            print(f"Error aprobarUsuario: {e}")
            return False

    @classmethod
    def borrarUsuario(cls, pNomUsuario, db):
        # 1. Buscar usuario usando buscarUsuarioDeLaListaParaAdmin
        usuario_a_borrar = cls.buscarUsuarioDeLaListaParaAdmin(pNomUsuario)

        # 2. Remover de memoria si existe
        if usuario_a_borrar:
            cls.listaUsuariosParaAdmin.remove(usuario_a_borrar)

        # 3. Ejecutar SQL DELETE
        try:
            sql = "DELETE FROM Usuario WHERE NombreUsuario = ?"
            db.delete(sql, (pNomUsuario,))
        except Exception as e:
            print(f"Error borrando usuario BD: {e}")

        # 4. Devolver la lista actualizada (diccionarios)
        lista_actualizada = []
        for u in cls.listaUsuariosParaAdmin:
            lista_actualizada.append({
                "nombre": u.getNombre(),
                "apellido": u.getApellido(),
                "nomUsuario": u.getNomUsuario(),
                "rol": u.rol
            })

        return lista_actualizada

    @classmethod
    def modificarUsuarioEnMemoriaPorAdmin(cls, pNomUsuarioOriginal, pNombre, pAp, pNomUsuarioModif, db):
        # 1. Buscar usuario
        usuario_act = cls.buscarUsuarioDeLaListaParaAdmin(pNomUsuarioOriginal)

        if usuario_act:
            # --- LÓGICA DE MEZCLA INTELIGENTE ---
            # Si el input viene vacío (falso), usamos el dato que ya tiene el objeto.
            final_nom = pNombre if pNombre and pNombre.strip() else usuario_act.getNombre()
            final_ap = pAp if pAp and pAp.strip() else usuario_act.getApellido()
            final_usuario = pNomUsuarioModif if pNomUsuarioModif and pNomUsuarioModif.strip() else usuario_act.getNomUsuario()

            # 2. Modificar datos en el objeto en memoria (usando los valores finales)
            usuario_act.modificarDatos(final_nom, final_ap, usuario_act.getCorreo(), final_usuario, None)

            # 3. Update SQL
            sql = "UPDATE Usuario SET NombreUsuario=?, Nombre=?, Apellido=? WHERE NombreUsuario=?"
            db.update(sql, (final_usuario, final_nom, final_ap, pNomUsuarioOriginal))

    def buscarUsuariosConFiltro(self, pNomUsuarioFiltro: str):
        """
        Pasos 7-16: Busca usuarios en BD, crea objetos temporales y devuelve lista de diccionarios.
        """
        usuarios_por_filtro = []  # Paso 9: ArrayList<Usuario>
        diccionario_usuarios = []

        # --- PASO 8: Obtener nombre de usuario explícitamente ---
        # Llamamos al método del usuario y guardamos el resultado en una variable local
        nomUsuario = self.usuario.getNomUsuario()

        # Pasos 10-11: SQL Query
        # Buscamos usuarios que coincidan con el filtro
        # Y que NO sean el propio usuario (NombreUsuario != ?)
        # Y que NO existan ya en la tabla AmigoDe (NOT EXISTS...)
        sql = """
              SELECT Nombre, Apellido, NombreUsuario
              FROM Usuario
              WHERE LOWER(NombreUsuario) LIKE ?
                AND NombreUsuario != ?
            AND NOT EXISTS (
                SELECT 1 FROM AmigoDe 
                WHERE NombreUsuario1 = ? AND NombreUsuario2 = Usuario.NombreUsuario
            )
            LIMIT 1000 \
              """

        # Preparamos el filtro con los comodines (%) para el LIKE
        wildcard = f"%{pNomUsuarioFiltro.lower()}%"

        # Ejecución SQL (Paso 11)
        # AHORA USAMOS LA VARIABLE 'nomUsuario' QUE OBTUVIMOS EN EL PASO 8
        # Orden de parámetros:
        # 1. wildcard -> para el LIKE
        # 2. nomUsuario -> para evitar listarse a uno mismo (NombreUsuario != ?)
        # 3. nomUsuario -> para comprobar si ya es amigo (NombreUsuario1 = ?)
        filas = self.db.select(sql, (wildcard, nomUsuario, nomUsuario))

        # Pasos 13-17: Recorrer resultados y crear objetos
        for fila in filas:
            # Paso 14-16: Extraer datos de la fila (ResultSet)
            nombre = fila['Nombre']
            apellido = fila['Apellido']
            nombre_usuario_bd = fila['NombreUsuario']

            # Paso 17: usuariosPorFiltro.add(new Usuario(...))
            # Creamos objetos Usuario temporales
            u_temp = Usuario(nombre, apellido, nombre_usuario_bd, "", "", "NOVERIF", [], self.db)
            usuarios_por_filtro.append(u_temp)

            # Preparar la salida JSON (Diccionarios para Jinja2)
            diccionario_usuarios.append({
                "nombre": u_temp.nombre,
                "apellido": u_temp.apellido,
                "NombreUsuario": u_temp.nombre_usuario,
                "es_amigo": False
            })

        return diccionario_usuarios

    def aniadirAmigo(self, pNomUsuarioAmigo: str) -> bool:
        """
        Pasos 19-25a: Coordina la adición en memoria y luego en BD.
        """
        # Paso 20: Llamada a Usuario.aniadirAmigo (Memoria)
        exito_memoria = self.usuario.aniadirAmigo(pNomUsuarioAmigo)

        if exito_memoria:
            # Paso 24a: Obtener nombre usuario actual
            nom_usuario_actual = self.usuario.getNomUsuario()

            # Paso 25a: execSQL INSERT en Base de Datos
            sql = "INSERT INTO AmigoDe (NombreUsuario1, NombreUsuario2) VALUES (?, ?)"
            try:
                self.db.insert(sql, (nom_usuario_actual, pNomUsuarioAmigo))
                return True
            except Exception as e:
                print(f"Error al añadir amigo en BD: {e}")
                # (Opcional) Si falla BD, se debería revertir memoria,
                # pero seguimos el diagrama estrictamente.
                return False

        return False  # Ya era amigo o error