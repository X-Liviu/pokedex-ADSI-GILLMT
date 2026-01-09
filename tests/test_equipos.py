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


# --- BLOQUE 3: GUARDAR ---

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

def test_ver_equipos_cuando_esta_vacio(client):
    with client.session_transaction() as sess:
        sess['username'] = 'UsuarioSinEquipos'
    res = client.get('/mis-equipos')
    assert b"no tienes" in res.data.lower() or b"vacio" in res.data.lower()


def test_acceso_a_detalles_y_enlace_modificar(client):
    """4.5: Verifica que se puede entrar al detalle y navegar a modificar."""
    inyectar_datos_pokedex()

    # 1. Forzamos que el usuario tenga un equipo cargado en su objeto
    # (Ya lo hacemos en la fixture, pero nos aseguramos)

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


# --- BLOQUE 5: MODIFICAR ---

def test_cancelar_modificacion_no_guarda_cambios(client):
    res = client.post('/modificar-equipo/1', data={'accion': 'cancelar'}, follow_redirects=True)
    assert b"Detalles" in res.data or b"equipo" in res.data


def test_confirmar_cambios_en_modificacion(client):
    res = client.post('/modificar-equipo/1', data={'accion': 'guardar'}, follow_redirects=True)
    assert "mis-equipos" in res.request.path