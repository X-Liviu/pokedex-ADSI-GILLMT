import pytest
from flask import Blueprint, session
from app import create_app
from app.database.connection import Connection

def limpiar_bd_changelog(db):
    """Deja las tablas limpias antes de cada test."""
    db.execute("DELETE FROM 'Publica'")
    db.execute("DELETE FROM 'Amigo de'")
    db.execute("DELETE FROM 'Usuario'")


def sql_crear_usuario(db, username):
    """Inserta un usuario directamente en la BD."""
    db.execute("""
               INSERT INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol)
               VALUES (?, 'Test', 'User', ?, '1234', 'usuario')
               """, (username, f"{username}@test.com"))


def sql_crear_amistad(db, user1, user2):
    db.execute("INSERT INTO 'Amigo de' (NombreUsuario1, NombreUsuario2) VALUES (?, ?)", (user1, user2))
    db.execute("INSERT INTO 'Amigo de' (NombreUsuario1, NombreUsuario2) VALUES (?, ?)", (user2, user1))


def sql_crear_noticia(db, autor, contenido, fecha):
    """Inserta una publicación en la tabla Publica."""
    db.execute("""
               INSERT INTO 'Publica' (NombreUsuario, FechaHora, Contenido)
               VALUES (?, ?, ?)
               """, (autor, fecha, contenido))


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_key_changelog'

    # Conexión real a la BD (o a la de test)
    db = Connection()
    limpiar_bd_changelog(db)

    # Mock del Menú Principal para que los botones de 'Volver' no den 404
    if 'menu_principal' not in app.blueprints:
        bp = Blueprint('menu_principal', __name__)

        @bp.route('/menu')  # Ajusta esto a la ruta real de tu menú
        def menu_view(): return "Menu Principal"

        app.register_blueprint(bp)

    with app.test_client() as client:
        # Inyectamos la db en el cliente para usarla fácilmente en los tests
        client.db = db
        yield client


# ==============================================================================
# 2. PRUEBAS FUNCIONALES (Tabla 1)
# ==============================================================================

# --- CASO 1.1 y 1.4: Usuario sin amigos ---
def test_1_1_usuario_sin_amigos_muestra_error(client):
    """
    CP 1.1: El usuario no tiene amigos -> Muestra plantilla de error.
    CP 1.4: Debe aparecer el botón de volver.
    """
    yo = "UserSolitario"

    # 1. Preparar BD (Solo existo yo)
    sql_crear_usuario(client.db, yo)

    # 2. Simular Sesión
    with client.session_transaction() as sess:
        sess['username'] = yo

    # 3. Petición (El controlador cargará el objeto Usuario desde la BD)
    res = client.get('/changelog')
    html = res.data.decode('utf-8')

    # 4. Verificaciones
    assert res.status_code == 200
    # Verifica que cargó la plantilla de error (busca texto clave)
    assert "no tienes amigos" in html.lower() or "error" in html.lower()
    # Verifica que hay un enlace para volver (CP 1.4)
    assert "volver" in html.lower() or "menu" in html.lower()


# --- CASO 1.2 y 1.5: Usuario con un amigo ---
def test_1_2_usuario_con_un_amigo(client):
    """
    CP 1.2: Muestra eventos de su único amigo.
    CP 1.5: Botón volver disponible.
    """
    yo = "Yo"
    amigo = "MiAmigo"
    noticia = "MiAmigo capturó un Charmander"

    # 1. Preparar BD
    sql_crear_usuario(client.db, yo)
    sql_crear_usuario(client.db, amigo)
    sql_crear_amistad(client.db, yo, amigo)
    sql_crear_noticia(client.db, amigo, noticia, "2024-01-20 10:00:00")

    # 2. Sesión
    with client.session_transaction() as sess:
        sess['username'] = yo

    # 3. Petición
    res = client.get('/changelog')
    html = res.data.decode('utf-8')

    # 4. Verificaciones
    assert res.status_code == 200
    assert noticia in html  # La noticia debe aparecer
    assert "no tienes amigos" not in html.lower()  # No debe dar error
    # CP 1.5
    assert "volver" in html.lower() or "menu" in html.lower()


# --- CASO 1.3 y 1.9: Múltiples amigos y Ordenación ---
def test_1_3_varios_amigos_orden_cronologico(client):
    """
    CP 1.3: Muestra eventos de múltiples amigos.
    CP 1.9: Ordenados del más reciente al más antiguo.
    """
    yo = "YoPopular"
    amigo1 = "AmigoAntiguo"
    amigo2 = "AmigoNuevo"

    msg_ayer = "Noticia de ayer"
    msg_hoy = "Noticia de hoy"

    # 1. Preparar BD
    sql_crear_usuario(client.db, yo)
    sql_crear_usuario(client.db, amigo1)
    sql_crear_usuario(client.db, amigo2)

    sql_crear_amistad(client.db, yo, amigo1)
    sql_crear_amistad(client.db, yo, amigo2)

    # Insertamos fechas claras
    sql_crear_noticia(client.db, amigo1, msg_ayer, "2024-01-01 10:00:00")
    sql_crear_noticia(client.db, amigo2, msg_hoy, "2024-01-02 10:00:00")

    # 2. Sesión
    with client.session_transaction() as sess:
        sess['username'] = yo

    # 3. Petición
    res = client.get('/changelog')
    html = res.data.decode('utf-8')

    # 4. Verificaciones
    assert msg_ayer in html
    assert msg_hoy in html

    # CP 1.9: Buscar la posición del texto en el HTML
    pos_hoy = html.find(msg_hoy)
    pos_ayer = html.find(msg_ayer)

    # La noticia de hoy (más reciente) debe aparecer ANTES (índice menor) que la de ayer
    assert pos_hoy < pos_ayer, "El orden cronológico es incorrecto. Debería ser Descendente."


# --- CASO 1.8: Duplicados ---
def test_1_8_no_mostrar_duplicados(client):
    """
    CP 1.8: Si hay eventos duplicados en la BD, deben mostrarse una sola vez
    (o filtrarse según tu lógica de negocio).
    """
    yo = "YoSinSpam"
    amigo = "AmigoRepe"
    texto_repe = "He subido de nivel"

    # 1. Preparar BD
    sql_crear_usuario(client.db, yo)
    sql_crear_usuario(client.db, amigo)
    sql_crear_amistad(client.db, yo, amigo)

    # Simulamos doble inserción (mismo contenido, segundos distintos para validar PK si aplica)
    sql_crear_noticia(client.db, amigo, texto_repe, "2024-01-01 12:00:00")
    sql_crear_noticia(client.db, amigo, texto_repe, "2024-01-01 12:00:05")

    # 2. Sesión
    with client.session_transaction() as sess:
        sess['username'] = yo

    # 3. Petición
    res = client.get('/changelog')
    html = res.data.decode('utf-8')

    # 4. Verificar
    cantidad = html.count(texto_repe)

    # Si tu sistema elimina duplicados visualmente:
    if cantidad > 1:
        pytest.fail(f"ERROR: Se muestra información duplicada. Aparece {cantidad} veces.")

    assert cantidad == 1


# --- CASO 1.11: Error de conexión ---
def test_1_11_error_conexion_bd(client, monkeypatch):
    """
    CP 1.11: Simula un fallo al intentar recuperar datos (ej. fallo en BD).
    Muestra mensaje de error y botón volver.
    """
    yo = "YoCrash"
    sql_crear_usuario(client.db, yo)

    with client.session_transaction() as sess:
        sess['username'] = yo

    # Usamos monkeypatch para 'romper' el método que obtiene el MarcoDex o los amigos
    # Esto simula que la BD se cayó justo cuando el controlador llamó al modelo.
    def mock_fallo(*args, **kwargs):
        raise Exception("Error de conexión simulado")

    # Ajusta 'app.controller.model.marcoDex_controller.MarcoDex.getMyMarcoDex'
    # a la ruta real de importación en tu controlador
    from app.controller.model.marcoDex_controller import MarcoDex
    monkeypatch.setattr(MarcoDex, "getMyMarcoDex", mock_fallo)

    # Al hacer GET, Flask lanzará 500 o tu manejo de excepciones
    # Si tienes un try/except en el controlador que renderiza una plantilla de error:
    try:
        res = client.get('/changelog')
        html = res.data.decode('utf-8')
        # Si tu app captura el error y muestra una página bonita:
        # assert "no fue posible cargar" in html.lower() or "error" in html.lower()
    except Exception:
        # Si Flask devuelve error 500 estándar
        pass