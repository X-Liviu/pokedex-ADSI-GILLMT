import pytest
import re
from flask import Blueprint, session
from app import create_app
from app.database.connection import Connection
from app.controller.model.gestorUsuario_controller import gestorUsuario
from app.model.usuario import Usuario


def limpiar_bd_changelog(db):
    db.execute("DELETE FROM 'Publica'")
    db.execute("DELETE FROM 'Amigo de'")
    db.execute("DELETE FROM 'Usuario'")


def insertar_usuario_sql(db, username):
    db.execute("""
               INSERT INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol)
               VALUES (?, 'Test', 'User', 'test@mail.com', '123', 'usuario')
               """, (username,))


def insertar_amistad_sql(db, user1, user2):
    """Crea la relación en la BD."""
    # Asumimos bidireccionalidad para asegurar que 'tiene_amigos()' funcione
    db.execute("INSERT INTO 'Amigo de' (NombreUsuario1, NombreUsuario2) VALUES (?, ?)", (user1, user2))
    db.execute("INSERT INTO 'Amigo de' (NombreUsuario1, NombreUsuario2) VALUES (?, ?)", (user2, user1))


def insertar_publicacion_sql(db, autor, contenido, fecha):
    """Inserta una noticia en la BD."""
    db.execute("""
               INSERT INTO 'Publica' (NombreUsuario, FechaHora, Contenido)
               VALUES (?, ?, ?)
               """, (autor, fecha, contenido))


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_changelog_key'

    db = Connection()
    limpiar_bd_changelog(db)

    if 'menu_principal' not in app.blueprints:
        bp = Blueprint('menu_principal', __name__)

        @bp.route('/menu-fake')
        def mostrar_menu(): return "Menu Principal"

        app.register_blueprint(bp)

    with app.test_client() as client:
        # Guardamos la referencia a la db en el cliente para usarla en los tests
        client.db = db
        yield client


def loguear_usuario(client, username):
    """
    1. Crea el usuario en BD.
    2. Lo inyecta en el singleton gestorUsuario (simulando el login).
    3. Establece la sesión de Flask.
    """
    db = client.db

    # A. Insertar en BD Física
    insertar_usuario_sql(db, username)

    # B. Inyectar en Memoria (Singleton) - SOLO EL USUARIO ACTIVO
    usuario_obj = Usuario(username, "Test", "User", "mail", "pass", "rol", [], db)

    # Limpiamos cualquier rastro anterior y ponemos solo a este usuario
    gestorUsuario._instancias_usuarios = {}
    gestor_mock = gestorUsuario(db, usuario_obj)
    gestorUsuario._instancias_usuarios[username] = gestor_mock

    # C. Sesión Flask
    with client.session_transaction() as sess:
        sess['username'] = username



# --- CASO 1.1 y 1.4: Usuario sin amigos ---
def test_usuario_sin_amigos_muestra_error(client):
    """
    CP 1.1: El usuario no tiene amigos -> Muestra mensaje/pantalla de error.
    CP 1.4: Debe haber opción para volver.
    """
    user = "Solitario"
    loguear_usuario(client, user)

    res = client.get('/changelog')
    html = res.data.decode('utf-8')

    # Verificaciones
    assert res.status_code == 200
    # Debe mostrar la plantilla de error (según tu controlador: 'error_no_amigos.html')
    assert "no tienes amigos" in html.lower() or "error" in html.lower()
    # CP 1.4: Verificar botón de volver (buscamos enlace o texto común)
    assert "volver" in html.lower() or "menu" in html.lower()


# --- CASO 1.2 y 1.5: Usuario con un amigo ---
def test_usuario_con_un_amigo(client):
    """
    CP 1.2: Muestra eventos de su único amigo.
    CP 1.5: Botón volver presente.
    """
    yo = "Yo"
    amigo = "Amigo1"
    evento = "Amigo1 ha ganado un torneo"

    # Setup
    loguear_usuario(client, yo)

    # Crear amigo en BD (pero NO en el gestor de memoria, solo en SQL)
    insertar_usuario_sql(client.db, amigo)
    insertar_amistad_sql(client.db, yo, amigo)
    insertar_publicacion_sql(client.db, amigo, evento, "2024-01-01 10:00:00")

    res = client.get('/changelog')
    html = res.data.decode('utf-8')

    assert res.status_code == 200
    assert evento in html
    assert "no tienes amigos" not in html.lower()
    # CP 1.5
    assert "volver" in html.lower() or "menu" in html.lower()


# --- CASO 1.3 y 1.9: Múltiples amigos y Orden ---
def test_varios_amigos_orden_cronologico(client):
    """
    CP 1.3: Muestra eventos mezclados de varios amigos.
    CP 1.9: Ordenados del más reciente al más antiguo.
    """
    yo = "YoPopular"
    amigo_old = "Viejo"
    amigo_new = "Nuevo"

    msg_viejo = "Evento del pasado"
    msg_nuevo = "Evento del futuro"

    loguear_usuario(client, yo)

    # Datos en BD
    insertar_usuario_sql(client.db, amigo_old)
    insertar_usuario_sql(client.db, amigo_new)

    insertar_amistad_sql(client.db, yo, amigo_old)
    insertar_amistad_sql(client.db, yo, amigo_new)

    # Insertamos fechas distintas
    insertar_publicacion_sql(client.db, amigo_old, msg_viejo, "2023-01-01 09:00:00")
    insertar_publicacion_sql(client.db, amigo_new, msg_nuevo, "2025-01-01 09:00:00")

    res = client.get('/changelog')
    html = res.data.decode('utf-8')

    # CP 1.3: Ambos aparecen
    assert msg_viejo in html
    assert msg_nuevo in html

    # CP 1.9: Verificar orden (El nuevo debe aparecer antes en el HTML)
    pos_nuevo = html.find(msg_nuevo)
    pos_viejo = html.find(msg_viejo)

    assert pos_nuevo != -1 and pos_viejo != -1
    assert pos_nuevo < pos_viejo, "El evento más reciente debería salir primero en la lista"


# --- CASO 1.8: Duplicados ---
def test_no_mostrar_duplicados(client):
    """
    CP 1.8: Existen eventos duplicados en la BD -> Se muestran una sola vez.
    """
    yo = "YoNoDupe"
    amigo = "AmigoBug"
    msg = "Mensaje Repetido"

    loguear_usuario(client, yo)
    insertar_usuario_sql(client.db, amigo)
    insertar_amistad_sql(client.db, yo, amigo)

    # Simulamos error de doble inserción en BD (diferente segundo para que la PK lo permita)
    insertar_publicacion_sql(client.db, amigo, msg, "2024-05-01 10:00:00")
    insertar_publicacion_sql(client.db, amigo, msg, "2024-05-01 10:00:01")

    res = client.get('/changelog')
    html = res.data.decode('utf-8')

    # Contamos apariciones del texto
    apariciones = html.count(msg)

    # NOTA: Esto pasará solo si tu lógica SQL usa 'DISTINCT' o filtro Python.
    # Si no tienes implementada la deduplicación, este test fallará (y te servirá para implementarlo).
    if apariciones > 1:
        pytest.fail(f"Se encontraron {apariciones} duplicados del mensaje, se esperaba 1.")
    else:
        assert apariciones == 1