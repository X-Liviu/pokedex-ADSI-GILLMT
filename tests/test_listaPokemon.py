import pytest
from app import create_app
from flask import Blueprint
from app.controller.model.pokeDex_controller import PokeDex
from app.model.especie import Especie
from app.controller.model.marcoDex_controller import MarcoDex
from app.model.usuario import Usuario
from app.database.connection import Connection # Aseguramos la importación

def inyectar_datos_pokedex():
    PokeDex._instance = None

    ##Especies

    especies = [
        Especie("Pikachu", "Raton", False, 0.4, 6.0, [], ["Electrico"], ""),
        Especie("Eevee", "Evolucion", False, 0.3, 6.5, [], ["Normal"], ""),
        Especie("Charmander", "Fuego", False, 0.6, 8.5, [], ["Fuego"], ""),
        Especie("Bulbasaur", "Semilla", False, 0.7, 6.9, ['Latigo Cepa'], ["Planta"], ""),
        Especie("Squirtle", "Tortuga", False, 0.5, 9.0, [], ["Agua"], ""),
        Especie("Caterpie", "Gusano", False, 0.3, 2.9, [], ["Bicho"], ""),
        Especie("Pidgey", "Pajaro", False, 0.3, 1.8, [], ["Volador"], "")
    ]
    return PokeDex.get_instance(especies)

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config['SECRET_KEY'] = 'test_laura'
    db = Connection()

    ##Crear usuario para las pruebas del menu principal
    # Registrar el menú principal para evitar errores de navegación
    if 'menu_principal_test' not in app.blueprints:
        bp = Blueprint('menu_principal', __name__)
        @bp.route('/menu_principal')
        def index():
            return "Menu Principal"

        app.register_blueprint(bp)

    # Limpiar instancias previas para evitar conflictos entre tests
    from app.controller.model.gestorUsuario_controller import gestorUsuario
    gestorUsuario._instancias_usuarios = {}

    # crear usuario invitado
    usuario_invitado = Usuario("Invitado", "Test", "invitado", "inv@test.com", "1234", "usuario", [], db)
    gestorUsuario._instancias_usuarios["Invitado"] = gestorUsuario(db, usuario_invitado)

    MarcoDex.getMyMarcoDex(db)

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["username"] = 'Invitado'
        yield client

## TESTS

def test1_1_mostrar_listaCompleta(client):
    inyectar_datos_pokedex()

    res = client.get("/lista_pokemon")
    assert b"Pikachu" in res.data
    assert b"Eevee" in res.data
    assert b"Bulbasaur" in res.data
    assert b"Charmander" in res.data
    assert b"Squirtle" in res.data
    assert b"Caterpie" in res.data
    assert b"Pidgey" in res.data

def test1_2_mostrarListaError(client):
    PokeDex._instance = None
    pokedex = PokeDex.get_instance([])
    pokedex.mostrarPokedex = lambda: "-1" ##poner a mano que devuelva un -1 (error tecnico)
    res = client.get('/lista_pokemon')

    assert b"Ha ocurrido un error" in res.data

def test1_3_volver(client):
    res = client.get('/menu_principal', follow_redirects=True)
    assert res.status_code == 200
    assert b"Menu Principal" in res.data
    assert res.request.path == "/menu_principal"

def test2_1_2_filtrarPokemon(client):
    #filtrar por nombre exacto y parcial
    inyectar_datos_pokedex()
    res_exacto = client.get('/lista_pokemon?filtro=nombre&valor=Pikachu')
    assert b"Pikachu" in res_exacto.data
    res_parcial = client.get('/lista_pokemon?filtro=nombre=pika')
    assert b"Pikachu" in res_parcial.data

def test2_3_nombreInexistente(client):
    inyectar_datos_pokedex()
    res = client.get('/lista_pokemon?filtro=nombre=marco')
    assert b"No se encontraron" in res.data or b"marco" not in res.data

def test2_4_nombreMinusculas(client):
    inyectar_datos_pokedex()
    res = client.get('/lista_pokemon?filtro=nombre&valor=pikachu')
    assert b"Pikachu" in res.data

def test2_5_nombreMayusculas(client):
    inyectar_datos_pokedex()
    res = client.get('/lista_pokemon?filtro=nombre&valor=PIKACHU')
    assert b"Pikachu" in res.data

def test2_6_nombreMinusculas(client):
    inyectar_datos_pokedex()
    res = client.get('/lista_pokemon?filtro=nombre&valor=pikachu')
    assert b"Pikachu" in res.data

def test2_7_filtroVacio(client):
    inyectar_datos_pokedex()
    res = client.get('/lista_pokemon?filtro=nombre&valor=')
    assert b"Pikachu" in res.data
    assert b"Eevee" in res.data
    assert b"Bulbasaur" in res.data
    assert b"Charmander" in res.data
    assert b"Squirtle" in res.data
    assert b"Caterpie" in res.data
    assert b"Pidgey" in res.data

def test2_8_caracteresEspeciales(client):
    inyectar_datos_pokedex()
    res = client.get('/lista_pokemon?filtro=nombre&valor=Pika$$$')
    assert b"No se encontraron" in res.data

def test2_9_cadenaLarga(client):
    inyectar_datos_pokedex()
    res = client.get('/lista_pokemon?filtro=nombre&valor=Pikahfgeghehnfndkfkfjiafaofhafhooeieiieieiehfikdkddidfhfhfhfj')
    assert b"No se encontraron" in res.data

def test2_10_conEspacios(client):
    inyectar_datos_pokedex()
    res = client.get('/lista_pokemon?filtro=nombre&valor=&20Pikachu%20')
    assert b"Pikachu" in res.data ## controlador necesita .strip()


def test3_1_mostrarDetalles(client):
    inyectar_datos_pokedex()
    res = client.get('/pokemon/Bulbasaur')
    assert res.status_code == 200

    html = res.data.decode('utf-8')

    assert "Bulbasaur" in html
    assert "Semilla" in html
    assert "Planta" in html
    assert "0.7" in html
    assert "6.9" in html
    assert "No" in html or "False" in html
    assert "Latigo Cepa" in html
    assert "" in html

def test3_2_mostrarDetallesError(client):
    inyectar_datos_pokedex()

    res = client.get('/pokemon/Missing')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert "Ha ocurrido un error" in html