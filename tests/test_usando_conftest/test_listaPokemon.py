import pytest
from app.controller.model.pokeDex_controller import PokeDex
from app.model.especie import Especie
from conftest import Connection

def inyectar_datos_pokedex():
    PokeDex._instance = None

    ##Especies

    especies = [
        Especie("Pikachu", "Raton", False, 0.4, 6.0, [], ["Electrico"], "",[],[]),
        Especie("Eevee", "Evolucion", False, 0.3, 6.5, [], ["Normal"], "",[],[]),
        Especie("Charmander", "Fuego", False, 0.6, 8.5, [], ["Fuego"], "",[],[]),
        Especie("Bulbasaur", "Semilla", False, 0.7, 6.9, ['Latigo Cepa'], ["Planta"], "",[],[]),
        Especie("Squirtle", "Tortuga", False, 0.5, 9.0, [], ["Agua"], "",[],[]),
        Especie("Caterpie", "Gusano", False, 0.3, 2.9, [], ["Bicho"], "",[],[]),
        Especie("Pidgey", "Pajaro", False, 0.3, 1.8, [], ["Volador"], "",[],[])
    ]
    return PokeDex.get_instance(especies)

def iniciar_sesion(p_cliente, pNombreUsuario: str):
    respuesta = p_cliente.post("/identificacion",
                               data={"usuario": pNombreUsuario, "contrasena": "1234"},
                               follow_redirects=True)
    assert respuesta.status_code == 200


## TESTS

def test1_1_mostrar_listaCompleta(client):
    iniciar_sesion(client, "LauraX")
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
    iniciar_sesion(client, "LauraX")
    PokeDex._instance = None
    pokedex = PokeDex.get_instance([])
    pokedex.mostrarPokedex = lambda: "-1" ##poner a mano que devuelva un -1 (error tecnico)
    res = client.get('/lista_pokemon')

    assert b"Ha ocurrido un error" in res.data

def test1_3_volver(client):
    iniciar_sesion(client, "LauraX")
    res = client.get('/menu', follow_redirects=True)
    assert res.status_code == 200
    assert res.request.path == "/menu"

def test2_1_2_filtrarPokemon(client):
    #filtrar por nombre exacto y parcial
    inyectar_datos_pokedex()
    res_exacto = client.get('/lista_pokemon?filtro=nombre&valor=Pikachu')
    assert b"Pikachu" in res_exacto.data
    res_parcial = client.get('/lista_pokemon?filtro=nombre=pika')
    assert b"Pikachu" in res_parcial.data

def test2_3_nombreInexistente(client):
    inyectar_datos_pokedex()
    iniciar_sesion(client, "LauraX")
    res = client.get('/lista_pokemon?filtro=nombre=marco')
    assert b"No se encontraron" in res.data or b"marco" not in res.data

def test2_4_nombreMinusculas(client):
    inyectar_datos_pokedex()
    iniciar_sesion(client, "LauraX")
    res = client.get('/lista_pokemon?filtro=nombre&valor=pikachu')
    assert b"Pikachu" in res.data

def test2_5_nombreMayusculas(client):
    inyectar_datos_pokedex()
    iniciar_sesion(client, "LauraX")
    res = client.get('/lista_pokemon?filtro=nombre&valor=PIKACHU')
    assert b"Pikachu" in res.data

def test2_6_nombreMinusculasyMayusculas(client):
    inyectar_datos_pokedex()
    iniciar_sesion(client, "LauraX")
    res = client.get('/lista_pokemon?filtro=nombre&valor=piKAchu')
    assert b"Pikachu" in res.data

def test2_7_filtroVacio(client):
    iniciar_sesion(client, "LauraX")
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
    iniciar_sesion(client, "LauraX")
    res = client.get('/lista_pokemon?filtro=nombre&valor=Pika$$$')
    assert b"No se encontraron" in res.data

def test2_9_cadenaLarga(client):
    inyectar_datos_pokedex()
    iniciar_sesion(client, "LauraX")
    res = client.get('/lista_pokemon?filtro=nombre&valor=Pikahfgeghehnfndkfkfjiafaofhafhooeieiieieiehfikdkddidfhfhfhfj')
    assert b"No se encontraron" in res.data

def test2_10_conEspacios(client):
    inyectar_datos_pokedex()
    iniciar_sesion(client, "LauraX")
    res = client.get('/lista_pokemon?filtro=nombre&valor=&20Pikachu%20')
    assert b"Pikachu" in res.data ## controlador necesita .strip()


def test3_1_mostrarDetalles(client):
    iniciar_sesion(client, "LauraX")
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
    iniciar_sesion(client, "LauraX")
    inyectar_datos_pokedex()

    res = client.get('/pokemon/Missing')
    assert b"Ha ocurrido un error" in res.data