import pytest
import sqlite3
import os

@pytest.fixture
def db_connection():
    """Obtiene una conexión directa a la base de datos de test (dbtest.sqlite)."""
    # Tu proyecto genera este archivo en la raíz para las pruebas
    db_path = os.path.join(os.getcwd(), "dbtest.sqlite")
    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()

@pytest.fixture
def setup_user_and_team(db_connection):
    """Prepara el usuario y las opciones del chatbot en la base de datos de test."""
    cursor = db_connection.cursor()
    # 1. Crear usuario de prueba (TestUser) [cite: 1009]
    cursor.execute("""
        INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol) 
        VALUES ('TestUser', 'Tester', 'ADSI', 'test@example.com', '1234', 'VERIF')
    """)
    # 2. Aseguramos que existan las opciones del chatbot según tu schema [cite: 1005]
    cursor.execute("INSERT OR IGNORE INTO OpcionChatbot VALUES ('1', 'Mejor Pokemon'), ('2', 'Tipos'), ('3', 'Evolucion'), ('4', 'Stats'), ('5', 'Salir')")
    db_connection.commit()
    return "TestUser"

# --- 1. SE ENTRA A LA INTERFAZ ---
def test_1_entrada_interfaz(client, setup_user_and_team):
    with client.session_transaction() as sess:
        sess['usuario'] = setup_user_and_team
    response = client.get('/chatbot')
    assert response.status_code == 200
    assert b"1 - Mejor Pokemon" in response.data

# --- 2. SE USA LA OPCIÓN 5 (SALIR) ---
def test_2_opcion_5_salir(client, setup_user_and_team):
    with client.session_transaction() as sess:
        sess['usuario'] = setup_user_and_team
        sess['estado'] = 'MENU'
    response = client.post('/chatbot', data={'mensaje': '5'})
    assert response.status_code == 302
    assert '/menu' in response.headers['Location']

# --- 3. SE INTRODUCE UNA OPCIÓN NO VÁLIDA ---
def test_3_opcion_no_valida(client, setup_user_and_team):
    with client.session_transaction() as sess:
        sess['estado'] = 'MENU'
        sess['menu_texto'] = "Menu"
    response = client.post('/chatbot', data={'mensaje': '99'}, follow_redirects=True)
    assert b"Opci\xc3\xb3n no v\xc3\xa1lida" in response.data

# --- 4. SE ELIGE LA OPCIÓN 1 SIN TENER EQUIPOS ---
def test_4_opcion_1_sin_equipos(client):
    with client.session_transaction() as sess:
        sess['usuario'] = 'UserSinNada'
        sess['estado'] = 'MENU'
    response = client.post('/chatbot', data={'mensaje': '1'}, follow_redirects=True)
    assert b"no dispones de equipos" in response.data

# --- 5. OPCIÓN 1 CON EQUIPO (BULBASAUR) E ID NO VÁLIDO ---
def test_5_opcion_1_id_invalido(client, db_connection, setup_user_and_team):
    cursor = db_connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO Equipo (idEquipo, NombreUsuario) VALUES (1, 'TestUser')")
    db_connection.commit()
    with client.session_transaction() as sess:
        sess['usuario'] = setup_user_and_team
        sess['estado'] = 'PARAMETRO'
        sess['opcion_activa'] = '1'
    response = client.post('/chatbot', data={'mensaje': '999'}, follow_redirects=True)
    assert b"No se han encontrado resultados" in response.data

# --- 6. OPCIÓN 1 CON EQUIPO (BULBASAUR) E ID VÁLIDO (1) ---
def test_6_opcion_1_id_valido(client, db_connection, setup_user_and_team):
    cursor = db_connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO Equipo (idEquipo, NombreUsuario) VALUES (1, 'TestUser')")
    # El ID 1 corresponde a Bulbasaur según la precarga de tu proyecto [cite: 164, 1110]
    cursor.execute("INSERT OR IGNORE INTO PokemonEnEquipo (idEquipoInterno, idPokemon) VALUES (1, 1)")
    db_connection.commit()
    with client.session_transaction() as sess:
        sess['usuario'] = setup_user_and_team
        sess['estado'] = 'PARAMETRO'
        sess['opcion_activa'] = '1'
    response = client.post('/chatbot', data={'mensaje': '1'}, follow_redirects=True)
    assert b"bulbasaur" in response.data.lower()

# --- 7. OPCIÓN 2 CON POKEMON NO VÁLIDO ---
def test_7_opcion_2_pokemon_no_valido(client):
    with client.session_transaction() as sess:
        sess['estado'] = 'PARAMETRO'
        sess['opcion_activa'] = '2'
    response = client.post('/chatbot', data={'mensaje': 'Inventamon'}, follow_redirects=True)
    assert b"No se han encontrado resultados" in response.data

# --- 8. OPCIÓN 2 CON POKEMON VÁLIDO (BULBASAUR) ---
def test_8_opcion_2_bulbasaur_valido(client):
    with client.session_transaction() as sess:
        sess['estado'] = 'PARAMETRO'
        sess['opcion_activa'] = '2'
    response = client.post('/chatbot', data={'mensaje': 'bulbasaur'}, follow_redirects=True)
    assert b"Informaci\xc3\xb3n encontrada" in response.data

# --- 9. OPCIÓN 3 CON POKEMON NO VÁLIDO ---
def test_9_opcion_3_pokemon_no_valido(client):
    with client.session_transaction() as sess:
        sess['estado'] = 'PARAMETRO'
        sess['opcion_activa'] = '3'
    response = client.post('/chatbot', data={'mensaje': 'PokemonFalso'}, follow_redirects=True)
    assert b"No se han encontrado resultados" in response.data

# --- 10. OPCIÓN 3 CON POKEMON VÁLIDO (BULBASAUR) ---
def test_10_opcion_3_bulbasaur_valido(client):
    with client.session_transaction() as sess:
        sess['estado'] = 'PARAMETRO'
        sess['opcion_activa'] = '3'
    response = client.post('/chatbot', data={'mensaje': 'bulbasaur'}, follow_redirects=True)
    # Bulbasaur tiene a Ivysaur en su cadena evolutiva precargada [cite: 1069, 1109]
    assert b"ivysaur" in response.data.lower()

# --- 11. OPCIÓN 4 CON POKEMON NO VÁLIDO ---
def test_11_opcion_4_pokemon_no_valido(client):
    with client.session_transaction() as sess:
        sess['estado'] = 'PARAMETRO'
        sess['opcion_activa'] = '4'
    response = client.post('/chatbot', data={'mensaje': 'NoExisteDex'}, follow_redirects=True)
    assert b"No se han encontrado resultados" in response.data

# --- 12. OPCIÓN 4 CON POKEMON VÁLIDO (BULBASAUR) ---
def test_12_opcion_4_bulbasaur_valido(client):
    with client.session_transaction() as sess:
        sess['estado'] = 'PARAMETRO'
        sess['opcion_activa'] = '4'
    response = client.post('/chatbot', data={'mensaje': 'bulbasaur'}, follow_redirects=True)
    # Altura de Bulbasaur en la precarga: 0.7 [cite: 123, 1231]
    assert b"0.7" in response.data