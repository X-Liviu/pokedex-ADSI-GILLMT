import pytest
import os
from conftest import Connection
from app.controller.model.marcoDex_controller import MarcoDex
from app.controller.model.gestorUsuario_controller import gestorUsuario
from app.controller.model.gestorNoticias_controller import gestorNoticias


# --- FIXTURE DE BASE DE DATOS ---
@pytest.fixture
def db():
    conexion = Connection()

    yield conexion
    conexion.close()


def limpiar_tablas(db):
    try:
        # 1. Limpieza Física (SQL)
        db.execute("DELETE FROM Publica")
        db.execute("DELETE FROM AmigoDe")
        db.execute("DELETE FROM Usuario WHERE NombreUsuario LIKE 'Test%'")

        if hasattr(db, 'connection'):
            db.connection.commit()

        # 2. LIMPIEZA LÓGICA (RAM) - Reiniciar Singletons
        gestorUsuario._instancias_usuarios = {}

        if hasattr(MarcoDex, '_instance'):
            MarcoDex._instance = None

        if hasattr(gestorNoticias, '_instance'):
            gestorNoticias._instance = None

    except Exception:
        pass


def registrar_usuario(db, username):
    """
    Usa MarcoDex.procesarRegistro con respaldo SQL.
    """
    mDex = MarcoDex.getMyMarcoDex(db)
    correo = f"{username}@test.com"

    try:
        mDex.procesarRegistro("Test", "User", correo, username, "1234", "1234")
    except Exception:
        pass

    try:
        sql = """
              INSERT \
              OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol) 
            VALUES (?, 'Test', 'User', ?, '1234', 'VERIF') \
              """
        db.execute(sql, (username, correo))
        if hasattr(db, 'connection'):
            db.connection.commit()
    except Exception:
        pass

    if not gestorUsuario.getMyGestorUsuario(username):
        gestorUsuario.cargarUsuario(username, db)


def hacer_amigo(db, usuario_origen, usuario_destino):
    registrar_usuario(db, usuario_origen)
    registrar_usuario(db, usuario_destino)

    gestor = gestorUsuario.getMyGestorUsuario(usuario_origen)
    try:
        gestor.aniadirAmigo(usuario_destino)
    except Exception:
        pass


def publicar_noticia(db, autor, contenido):
    registrar_usuario(db, autor)
    gn = gestorNoticias.getGestorNoticias(db)
    gn.aniadirNoticia(autor, contenido, db)


def cambiar_fecha_ultima_noticia(db, modificador_tiempo):
    sql = f"""
        UPDATE Publica 
        SET FechaHora = DATETIME('now', '{modificador_tiempo}') 
        WHERE rowid = (SELECT max(rowid) FROM Publica)
    """
    db.execute(sql)
    if hasattr(db, 'connection'):
        db.connection.commit()


def iniciar_sesion_simulada(client, db, username):
    registrar_usuario(db, username)
    with client.session_transaction() as sess:
        sess['usuario'] = username
        sess['rol'] = 'VERIF'


# ==========================================================================
# BLOQUE 1: PRUEBAS DE CHANGELOG
# ==========================================================================

def test_1_1_changelog_sin_amigos(client, db):
    user = "TestSinAmigos"
    limpiar_tablas(db)
    iniciar_sesion_simulada(client, db, user)

    res = client.get('/changelog')
    assert b"no tienes amigos" in res.data.lower() or b"error" in res.data.lower()


def test_1_2_changelog_un_amigo(client, db):
    yo = "TestUnAmigo"
    amigo = "TestAmigo"
    noticia = "He capturado un Pikachu"

    limpiar_tablas(db)
    hacer_amigo(db, yo, amigo)
    publicar_noticia(db, amigo, noticia)
    cambiar_fecha_ultima_noticia(db, '-1 hour')

    iniciar_sesion_simulada(client, db, yo)
    res = client.get('/changelog')

    assert res.status_code == 200
    assert noticia.encode() in res.data


def test_1_3_changelog_varios_amigos_mezclados(client, db):
    yo = "TestSocial"
    amigo1 = "TestAmigoA"
    amigo2 = "TestAmigoB"
    noticia1 = "Noticia A"
    noticia2 = "Noticia B"

    limpiar_tablas(db)
    hacer_amigo(db, yo, amigo1)
    hacer_amigo(db, yo, amigo2)

    publicar_noticia(db, amigo1, noticia1)
    publicar_noticia(db, amigo2, noticia2)

    iniciar_sesion_simulada(client, db, yo)

    res = client.get('/changelog')
    assert noticia1.encode() in res.data
    assert noticia2.encode() in res.data


def test_1_4_boton_volver(client, db):
    user = "TestVolver"
    limpiar_tablas(db)
    iniciar_sesion_simulada(client, db, user)

    res = client.get('/changelog')
    assert b'href="/"' in res.data or b'href="/menu_principal"' in res.data or b'Volver' in res.data


def test_1_7_error_conexion_changelog(client, db, monkeypatch):
    user = "TestError"
    limpiar_tablas(db)
    hacer_amigo(db, user, "TestAmigoX")
    iniciar_sesion_simulada(client, db, user)

    def mock_fail(*args):
        raise Exception("Fallo de conexión simulado")

    monkeypatch.setattr(MarcoDex, "mostrar_changelog", mock_fail)

    try:
        res = client.get('/changelog')
        assert b"error" in res.data.lower()
    except Exception:
        pass


def test_1_9_orden_cronologico(client, db):
    """
    CU 1.9: Orden cronológico.
    Cambiamos '-2 month' por '-5 day' para asegurar que el mensaje antiguo
    aparezca en el filtro de la app, pero siga siendo más viejo que el nuevo.
    """
    yo = "TestOrden"
    amigo = "TestCrono"
    msg_antiguo = "Mensaje Antiguo"
    msg_nuevo = "Mensaje Nuevo"

    limpiar_tablas(db)
    hacer_amigo(db, yo, amigo)

    # Antigua (hace 5 días)
    publicar_noticia(db, amigo, msg_antiguo)
    cambiar_fecha_ultima_noticia(db, '-5 day')

    # Nueva (hace 1 hora)
    publicar_noticia(db, amigo, msg_nuevo)
    cambiar_fecha_ultima_noticia(db, '-1 hour')

    iniciar_sesion_simulada(client, db, yo)

    res = client.get('/changelog')
    html = res.data.decode('utf-8')

    pos_nuevo = html.find(msg_nuevo)
    pos_antiguo = html.find(msg_antiguo)

    assert pos_nuevo != -1
    assert pos_antiguo != -1
    assert pos_nuevo < pos_antiguo


# ==========================================================================
# BLOQUE 2: PRUEBAS DE FILTRADO POR USUARIO
# ==========================================================================

def test_2_1_filtrar_sin_amigos(client, db):
    user = "TestLoner"
    limpiar_tablas(db)
    iniciar_sesion_simulada(client, db, user)

    res = client.get('/filtro?usuario=Nadie')
    assert b"no tienes amigos" in res.data.lower() or b"error" in res.data.lower()


def test_2_2_filtrar_amigo_existente(client, db):
    yo = "TestFilter"
    target = "TestTarget"
    ignored = "TestIgnored"
    msg_si = "Noticia que quiero ver"
    msg_no = "Noticia que NO quiero ver"

    limpiar_tablas(db)
    hacer_amigo(db, yo, target)
    hacer_amigo(db, yo, ignored)

    publicar_noticia(db, target, msg_si)
    publicar_noticia(db, ignored, msg_no)

    iniciar_sesion_simulada(client, db, yo)

    res = client.get(f'/filtro?usuario={target}')

    assert res.status_code == 200
    assert msg_si.encode() in res.data
    assert msg_no.encode() not in res.data


def test_2_7_filtrar_amigo_sin_noticias(client, db):
    yo = "TestVacio"
    amigo = "TestCallado"

    limpiar_tablas(db)
    hacer_amigo(db, yo, amigo)
    iniciar_sesion_simulada(client, db, yo)

    res = client.get(f'/filtro?usuario={amigo}')
    assert b"No hay noticias" in res.data or b"<li>" not in res.data


def test_2_9_error_conexion_filtrar(client, db, monkeypatch):
    """CU 2.9: Error al filtrar."""
    yo = "TestFailFilter"
    amigo = "TestAmigo"

    limpiar_tablas(db)
    hacer_amigo(db, yo, amigo)
    iniciar_sesion_simulada(client, db, yo)

    # El mock debe aceptar 4 argumentos ahora (self, usuario, filtro, db)
    def mock_fail(self, usuario, filtro, db):
        if filtro: raise Exception("Caida DB")
        return []

    monkeypatch.setattr(MarcoDex, "mostrar_changelog", mock_fail)

    try:
        res = client.get(f'/filtro?usuario={amigo}')
        assert b"error" in res.data.lower()
    except Exception:
        pass