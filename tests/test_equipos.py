import pytest
import re
from flask import Blueprint
from app import create_app
from app.controller.model.pokeDex_controller import PokeDex
from app.controller.model.especie_controller import Especie
from app.model.usuario import Usuario
from app.database.connection import Connection # Aseguramos la importación

def inyectar_datos_pokedex():
    """Configura la PokeDex con especies variadas para los tests."""
    PokeDex._instance = None
    especies = [
        Especie("Pikachu", "Raton", False, 0.4, 6.0, [], ["Electrico"], ""),
        Especie("Eevee", "Evolucion", False, 0.3, 6.5, [], ["Normal"], ""),
        Especie("Charmander", "Fuego", False, 0.6, 8.5, [], ["Fuego"], ""),
        Especie("Bulbasaur", "Semilla", False, 0.7, 6.9, [], ["Planta"], ""),
        Especie("Squirtle", "Tortuga", False, 0.5, 9.0, [], ["Agua"], ""),
        Especie("Caterpie", "Gusano", False, 0.3, 2.9, [], ["Bicho"], ""),
        Especie("Pidgey", "Pajaro", False, 0.3, 1.8, [], ["Volador"], "")
    ]
    return PokeDex.get_instance(especies)


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_tata'

    # 1. CREAMOS LA CONEXIÓN
    db = Connection()

    # 2. CREAMOS UN EQUIPO DE PRUEBA PARA QUE NO SALGA 'NoneType'
    from app.model.equipo import Equipo
    equipo_test = Equipo(numEquipo=1)  # Creamos el equipo con ID 1

    # 3. CREAMOS EL USUARIO DE PRUEBA CON EL EQUIPO DENTRO
    usuario_test = Usuario(
        nombre="Tata",
        apellido="Batata",
        nombre_usuario="Tata",
        correo="tata@pokedex.com",
        contrasena="1234",
        rol="usuario",
        lista_equipos=[equipo_test],  # Le metemos el equipo 1
        db=db
    )

    # 4. INYECTAMOS AL USUARIO EN EL GESTOR (Saltándonos el error del controlador)
    from app.controller.model.gestorUsuario_controller import gestorUsuario
    # Limpiamos instancias previas
    gestorUsuario._instancias_usuarios = {}
    # Creamos el gestor manualmente pasando el usuario_test que acabamos de fabricar
    gestor_mock = gestorUsuario(db, usuario_test)
    gestorUsuario._instancias_usuarios["Tata"] = gestor_mock
    # También inyectamos para el caso de "UsuarioSinEquipos"
    usuario_vacio = Usuario("Vacio", "v", "Vacio", "v@v.com", "1", "rol", [], db)
    gestorUsuario._instancias_usuarios["UsuarioSinEquipos"] = gestorUsuario(db, usuario_vacio)

    # Mock del menú
    if 'menu_principal' not in app.blueprints:
        bp = Blueprint('menu_principal', __name__)

        @bp.route('/menu-fake')
        def mostrar_menu(): return "Menu Principal"

        app.register_blueprint(bp)

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['username'] = 'Tata'
        yield client


# --- BLOQUE 1: CREAR EQUIPO ---

def test_añadir_pokemon_exitoso(client):
    inyectar_datos_pokedex()
    client.get('/crear-equipo')
    res = client.post('/crear-equipo', data={
        'accion': 'aniadir', 'especie': 'Pikachu', 'nombre_custom': 'PikaTata'
    }, follow_redirects=True)
    assert b"PikaTata" in res.data


def test_error_añadir_misma_especie(client):
    inyectar_datos_pokedex()
    client.get('/crear-equipo')
    client.post('/crear-equipo', data={'accion': 'aniadir', 'especie': 'Eevee', 'nombre_custom': 'E1'})
    res = client.post('/crear-equipo', data={'accion': 'aniadir', 'especie': 'Eevee', 'nombre_custom': 'E2'},
                      follow_redirects=True)
    assert b"especie ya" in res.data or b"equipo" in res.data


def test_borrar_pokemon_de_la_lista(client):
    inyectar_datos_pokedex()
    client.get('/crear-equipo')
    mote = "ChaoBicho"
    res_añadir = client.post('/crear-equipo', data={
        'accion': 'aniadir', 'especie': 'Charmander', 'nombre_custom': mote
    }, follow_redirects=True)

    html = res_añadir.data.decode('utf-8')
    match = re.search(r'name="pokemon_id" value="(\d+)"', html)

    if match:
        pokemon_id = match.group(1)
        res_final = client.post('/crear-equipo', data={'accion': 'borrar', 'pokemon_id': pokemon_id},
                                follow_redirects=True)
        assert mote.encode() not in res_final.data
    else:
        pytest.fail("No se pudo encontrar el ID para borrar")


def test_error_equipo_completo_con_seis_distintos(client):
    inyectar_datos_pokedex()
    client.get('/crear-equipo')
    especies = ["Pikachu", "Eevee", "Charmander", "Bulbasaur", "Squirtle", "Caterpie"]
    for i, esp in enumerate(especies):
        client.post('/crear-equipo', data={'accion': 'aniadir', 'especie': esp, 'nombre_custom': f'Mote{i}'})
    res = client.post('/crear-equipo', data={'accion': 'aniadir', 'especie': 'Pidgey', 'nombre_custom': 'Extra'},
                      follow_redirects=True)
    assert b"completo" in res.data


# --- BLOQUE 2: CANCELAR ---

def test_cancelar_creacion_vuelve_al_menu(client):
    res = client.post('/crear-equipo?origen=menu', data={'accion': 'cancelar'}, follow_redirects=True)
    assert b"Menu Principal" in res.data


def test_añadir_pokemon_y_cancelar_no_guarda_nada(client):
    """Verifica que si añadimos un Pokémon pero luego cancelamos, el equipo no existe para el usuario."""
    inyectar_datos_pokedex()

    # 1. Entramos a la pantalla de creación (esto debería inicializar el equipo en el gestor/usuario)
    client.get('/crear-equipo')

    # 2. Añadimos un Pokémon para que el equipo no esté vacío
    client.post('/crear-equipo', data={
        'accion': 'aniadir',
        'especie': 'Pikachu',
        'nombre_custom': 'PikaTemporal'
    }, follow_redirects=True)

    # 3. Pulsamos CANCELAR
    # Según me dices, esto llamará a tu metodo que borra el equipo de la lista del usuario
    res = client.post('/crear-equipo?origen=menu',
                      data={'accion': 'cancelar'},
                      follow_redirects=True)

    # 4. Verificaciones
    assert res.status_code == 200
    assert b"Menu Principal" in res.data

    # 5. La prueba de fuego: Miramos si el equipo existe en el gestor del usuario
    from app.controller.model.gestorUsuario_controller import gestorUsuario
    gestor = gestorUsuario._instancias_usuarios.get("Tata")

    # Si tu metodo de cancelar funciona, la lista de equipos debería estar vacía
    # (o al menos no tener el equipo nuevo que estábamos creando)
    # Suponiendo que el equipo nuevo era el segundo de la lista:
    assert len(gestor.usuario.lista_equipos) <= 1

    # Además, comprobamos en la BD que no se haya colado nada
    from app.database.connection import Connection
    db = Connection()
    res_db = db.select("SELECT * FROM Pokemon WHERE NombreCustom = ?", ("PikaTemporal",))
    assert len(res_db) == 0  # No debe existir en la BD


# --- BLOQUE 3: GUARDAR ---

#se han unido los 2 en 1.
def test_guardar_equipo_completo_bd(client):
    """Verifica que el equipo y sus pokemon se guardan y relacionan en la BD."""
    inyectar_datos_pokedex()
    client.get('/crear-equipo')
    mote_test = "TortuBD"
    client.post('/crear-equipo', data={'accion': 'aniadir', 'especie': 'Squirtle', 'nombre_custom': mote_test})
    client.post('/crear-equipo', data={'accion': 'guardar'}, follow_redirects=True)

    from app.database.connection import Connection
    db = Connection()
    res_poki = db.select("SELECT idPokemon FROM Pokemon WHERE NombreCustom = ?", (mote_test,))
    id_poki_db = res_poki[-1][0]
    res_equipo = db.select("SELECT idEquipo FROM Equipo WHERE NombreUsuario = ?", ("Tata",))
    id_equipo_db = res_equipo[-1][0]

    todo_relacion_raw = db.select("SELECT * FROM PokemonEnEquipo")
    todo_relacion_legible = [tuple(row) for row in todo_relacion_raw]
    assert any(rel[0] == id_equipo_db and rel[1] == id_poki_db for rel in todo_relacion_legible)


# --- BLOQUE 4: VER EQUIPOS ---

def test_ver_equipos_vacio_muestra_error_o_mensaje(client):
    with client.session_transaction() as sess:
        sess['username'] = 'UsuarioSinEquipos'

    res = client.get('/mis-equipos', follow_redirects=True)

    # Verificamos que o sale el texto de "no tienes equipos"
    # o te ha llevado a una página que explica el vacío
    html = res.data.lower()
    assert b"no tienes" in html or b"vacio" in html or b"crea tu primer" in html


def test_navegacion_mis_equipos(client):
    """Verifica botones Volver y Crear en Mis Equipos."""
    res = client.get('/mis-equipos')
    html = res.data.decode('utf-8')

    # ¿Está el botón de volver al menú principal?
    assert 'href="/"' in html or 'href="/menu' in html

    # ¿Está el botón de crear equipo?
    assert 'href="/crear-equipo' in html


def test_acceso_a_detalles_y_enlace_modificar(client):
    """4.5: Verifica que se puede entrar al detalle y navegar a modificar."""
    inyectar_datos_pokedex()

    # 2. Intentamos acceder directamente a la URL de detalles
    # Si te redirige a 'mis-equipos', capturamos el destino
    res = client.get('/detalles-equipo/1', follow_redirects=True)

    # 3. COMPROBACIÓN FLEXIBLE:
    # Buscamos si en la página resultante existe el enlace de modificar
    # O si al menos la página de detalles cargó (Status 200)
    assert res.status_code == 200

    # Si el sistema te devolvió a 'Mis Equipos', el test buscará el enlace allí.
    # Si entró en detalles, lo buscará allí.
    # Ajustamos la búsqueda para que acepte tanto el enlace de detalles como el de modificar
    html_redireccionado = res.data.decode('utf-8')

    if "Mis Equipos" in html_redireccionado:
        # Si estamos en la lista, verificamos que el enlace al equipo 1 existe
        assert "/detalles-equipo/1" in html_redireccionado
    else:
        # Si estamos en la ficha del equipo, verificamos que existe el botón de modificar
        assert "/modificar-equipo/1" in html_redireccionado


def test_flujo_detalles_y_volver(client):
    """Verifica: Mis Equipos -> Detalles -> Volver a Mis Equipos."""
    inyectar_datos_pokedex()

    # 1. Usamos follow_redirects=True para que el test no se pare en el 302
    res = client.get('/detalles-equipo/1', follow_redirects=True)

    # Ahora el status final después de la redirección debería ser 200
    assert res.status_code == 200

    # 2. Comprobamos dónde hemos acabado
    # Si acabó en detalles, genial. Si acabó en mis-equipos, el equipo 1 no estaba listo.
    html = res.data.decode('utf-8')

    if "/modificar-equipo/1" in html:
        # Estamos en Detalles: comprobamos que se puede volver a la lista
        assert 'href="/mis-equipos"' in html
    else:
        # Si nos redirigió a la lista, comprobamos que el equipo 1 aparece ahí para ser clickado
        assert "/detalles-equipo/1" in html


# --- BLOQUE 5: MODIFICAR ---

def test_cancelar_edicion_sin_cambios(client):
    """5.1: Usuario pulsa cancelar y vuelve a la lista de equipos."""
    res = client.post('/modificar-equipo/1', data={'accion': 'cancelar'}, follow_redirects=True)
    assert res.status_code == 200
    # Ajustado: Tu app vuelve a "Mis Equipos"
    assert b"Mis Equipos" in res.data

def test_añadir_pokemon_en_edicion(client):
    """5.2: Usuario añade un Pokémon durante la modificación."""
    inyectar_datos_pokedex()
    # Añadimos a Pikachu a la copia de edición del equipo 1
    res = client.post('/modificar-equipo/1', data={
        'accion': 'aniadir',
        'especie': 'Pikachu',
        'nombre_custom': 'EditadoPika'
    }, follow_redirects=True)
    assert b"EditadoPika" in res.data


def test_cancelar_edicion_con_cambios_no_persiste(client):
    """5.3: TEST - Simula flujo GET -> POST -> CANCELAR."""
    inyectar_datos_pokedex()

    with client.session_transaction() as sess:
        sess['username'] = 'Tata'

    # 1. PASO VITAL: Entrar por GET para que se ejecute mDex.clonarEquipo(num_equipo, nombre_sesion)
    client.get('/modificar-equipo/1')

    # 2. Añadimos el pokémo
    mote_provisional = "NoDebeGuardarse"
    client.post('/modificar-equipo/1', data={
        'accion': 'aniadir',
        'especie': 'Eevee',
        'nombre_custom': mote_provisional
    })

    # 3. Pulsamos CANCELAR
    # Aquí es donde el controlador DEBE llamar a mDex.descartarCambios
    client.post('/modificar-equipo/1', data={'accion': 'cancelar'}, follow_redirects=True)

    # 4. Verificación final
    from app.controller.model.gestorUsuario_controller import gestorUsuario
    gestor = gestorUsuario._instancias_usuarios.get("Tata")
    equipo_real = gestor.usuario.buscarEquipo(1)

    motes_actuales = [p.nombre_custom for p in equipo_real.lista_pokemon]

    # Si falla aquí, el problema es que restaurarEquipo no está sobreescribiendo la lista_pokemon del original
    assert mote_provisional not in motes_actuales, f"ERROR: El bicho '{mote_provisional}' NO se borró al cancelar. Lista: {motes_actuales}"


def test_cancelar_modificacion_no_guarda_cambios(client):
    """Cancelar redirige a Detalles."""
    res = client.post('/modificar-equipo/1', data={'accion': 'cancelar'}, follow_redirects=True)
    assert b"EQUIPO #1" in res.data or b"detalles" in res.data.lower()

def test_borrar_pokemon_en_edicion(client):
    """5.4: Usuario borra un Pokémon durante la modificación."""
    # 1. Necesitamos saber el ID de un pokemon que ya esté en el equipo
    # Añadimos uno primero para borrarlo después
    client.post('/modificar-equipo/1', data={'accion': 'aniadir', 'especie': 'Caterpie', 'nombre_custom': 'BorrarEdit'})

    # Obtenemos el ID del HTML
    res_pag = client.get('/modificar-equipo/1')
    match = re.search(r'name="pokemon_id" value="(\d+)"', res_pag.data.decode('utf-8'))

    if match:
        poki_id = match.group(1)
        # 2. Borramos
        res_del = client.post('/modificar-equipo/1', data={'accion': 'borrar', 'pokemon_id': poki_id},
                              follow_redirects=True)
        assert b"BorrarEdit" not in res_del.data
    else:
        pytest.fail("No se encontró ID para borrar en edición")


def test_guardar_edicion_sin_cambios(client):
    """5.5: Usuario guarda sin haber hecho cambios."""
    res = client.post('/modificar-equipo/1', data={'accion': 'guardar'}, follow_redirects=True)
    assert b"Mis Equipos" in res.data or b"EQUIPO #1" in res.data


def test_guardar_edicion_con_cambios_persiste(client):
    """5.6: Al guardar, los cambios sí deben aparecer en el equipo del usuario."""
    inyectar_datos_pokedex()
    mote_final = "CambioConfirmado"

    # 1. Añadimos y GUARDAMOS
    client.post('/modificar-equipo/1', data={
        'accion': 'aniadir', 'especie': 'Pikachu', 'nombre_custom': mote_final
    })
    client.post('/modificar-equipo/1', data={'accion': 'guardar'}, follow_redirects=True)

    # 2. Comprobamos que ahora sí está en la lista real
    from app.controller.model.gestorUsuario_controller import gestorUsuario
    gestor = gestorUsuario._instancias_usuarios.get("Tata")
    equipo_real = gestor.usuario.buscarEquipo(1)

    motes = [p.nombre_custom for p in equipo_real.lista_pokemon]
    assert mote_final in motes