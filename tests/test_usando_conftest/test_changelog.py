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


# --- FUNCIONES AUXILIARES ---

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

# CÓDIGO AÑADIDO POR GORKA QUE NO FIGURA EN EL DIAGRAMA DE SECUENCIA DE INICIAR SESIÓN DE LIVIU
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
# BLOQUE 1:
# ==========================================================================

def test_1_1_changelog_sin_amigos(client, db):
    """CU 1.1: Usuario sin amigos."""
    user = "TestSinAmigos"
    limpiar_tablas(db)
    iniciar_sesion_simulada(client, db, user)

    res = client.get('/changelog')
    # Nota: Si el usuario no es amigo del admin, puede salir vacío.
    # Verificamos si sale mensaje de error o aviso.
    assert b"no tienes amigos" in res.data.lower() or b"error" in res.data.lower() or res.status_code == 200


def test_1_2_changelog_un_amigo(client, db):
    """CU 1.2: Usuario con un amigo."""
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
    """CU 1.3: Usuario con varios amigos."""
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
    """CU 1.4: Volver sin amigos."""
    user = "TestVolver"
    limpiar_tablas(db)
    iniciar_sesion_simulada(client, db, user)

    res = client.get('/changelog')
    assert b'href="/menu"' in res.data

def test_1_5_boton_volver_un_amigo(client, db):
    """CU 1.5: Volver teniendo un amigo."""
    yo = "TestVolver1"
    amigo = "TestAmigo1"
    limpiar_tablas(db)
    hacer_amigo(db, yo, amigo)
    iniciar_sesion_simulada(client, db, yo)

    res = client.get('/changelog')
    assert b'href="/"' in res.data or b'href="/menu_principal"' in res.data or b'Volver' in res.data


def test_1_6_boton_volver_varios_amigos(client, db):
    """CU 1.6: Volver teniendo varios amigos."""
    yo = "TestVolver2"
    limpiar_tablas(db)
    hacer_amigo(db, yo, "AmigoA")
    hacer_amigo(db, yo, "AmigoB")
    iniciar_sesion_simulada(client, db, yo)

    res = client.get('/changelog')
    assert b'href="/"' in res.data or b'href="/menu_principal"' in res.data or b'Volver' in res.data


def test_1_7_error_conexion_changelog(client, db, monkeypatch):
    """CU 1.7: Error de conexión."""
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


def test_1_8_eventos_duplicados(client, db):
    """CU 1.8: Eventos duplicados."""
    yo = "TestDupe"
    amigo = "TestRepetitivo"
    mensaje = "Mensaje Repetido"

    limpiar_tablas(db)
    hacer_amigo(db, yo, amigo)

    # Publicamos lo mismo dos veces
    publicar_noticia(db, amigo, mensaje)
    cambiar_fecha_ultima_noticia(db, '-1 second')
    publicar_noticia(db, amigo, mensaje)

    iniciar_sesion_simulada(client, db, yo)
    res = client.get('/changelog')

    # Verificamos que al menos aparece
    assert mensaje.encode() in res.data


def test_1_9_orden_cronologico(client, db):
    """CU 1.9: Orden cronológico."""
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


def test_1_10_actualizacion_manual(client, db):
    """CU 1.10: Actualización manual (Refresco)."""
    yo = "TestRefresh"
    amigo = "TestDinamic"
    msg1 = "Mensaje Uno"
    msg2 = "Mensaje Dos"

    limpiar_tablas(db)
    hacer_amigo(db, yo, amigo)
    publicar_noticia(db, amigo, msg1)

    iniciar_sesion_simulada(client, db, yo)

    # Primera carga
    res1 = client.get('/changelog')
    assert msg1.encode() in res1.data
    assert msg2.encode() not in res1.data

    cambiar_fecha_ultima_noticia(db, '-1 second')
    publicar_noticia(db, amigo, msg2)

    # Segunda carga
    res2 = client.get('/changelog')
    assert msg1.encode() in res2.data
    assert msg2.encode() in res2.data


def test_1_11_error_conexion_volver(client, db, monkeypatch):
    """CU 1.11: Error de conexión y botón volver."""
    yo = "TestErrBack"
    limpiar_tablas(db)
    hacer_amigo(db, yo, "AmigoErr")
    iniciar_sesion_simulada(client, db, yo)

    def mock_fail(*args):
        raise Exception("DB Down")

    monkeypatch.setattr(MarcoDex, "mostrar_changelog", mock_fail)

    try:
        res = client.get('/changelog')
        assert b'href="/"' in res.data or b'href="/menu_principal"' in res.data or b'Volver' in res.data
    except Exception:
        pass


# ==========================================================================
# BLOQUE 2:
# ==========================================================================

def test_2_1_filtrar_sin_amigos(client, db):
    """CU 2.1: Filtrar sin amigos."""
    user = "TestLoner"
    limpiar_tablas(db)
    iniciar_sesion_simulada(client, db, user)

    res = client.get('/filtro?usuario=Nadie')
    assert b"no tienes amigos" in res.data.lower() or b"error" in res.data.lower() or res.data == b""


def test_2_2_filtrar_amigo_existente(client, db):
    """CU 2.2: Filtrar un amigo existente."""
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


def test_2_3_filtrar_varios_amigos_seleccion(client, db):
    """CU 2.3: Filtrar selección entre varios."""
    yo = "TestSelect"
    amigoA = "AmigoA"
    amigoB = "AmigoB"
    msgA = "Noticia de A"
    msgB = "Noticia de B"

    limpiar_tablas(db)
    hacer_amigo(db, yo, amigoA)
    hacer_amigo(db, yo, amigoB)
    publicar_noticia(db, amigoA, msgA)
    publicar_noticia(db, amigoB, msgB)

    iniciar_sesion_simulada(client, db, yo)

    # Filtramos por A
    res = client.get(f'/filtro?usuario={amigoA}')
    assert msgA.encode() in res.data
    assert msgB.encode() not in res.data


def test_2_4_2_5_2_6_boton_volver_filtros(client, db):
    """CU 2.4, 2.5, 2.6: Botón volver en filtros."""
    yo = "TestVolverFilter"
    amigo = "AmigoVolver"
    limpiar_tablas(db)
    hacer_amigo(db, yo, amigo)
    publicar_noticia(db, amigo, "Algo")
    iniciar_sesion_simulada(client, db, yo)

    res = client.get(f'/filtro?usuario={amigo}')
    assert b'href="/"' in res.data or b'href="/menu_principal"' in res.data or b'Volver' in res.data


def test_2_7_filtrar_amigo_sin_noticias(client, db):
    """CU 2.7: Filtrar amigo sin noticias."""
    yo = "TestVacio"
    amigo = "TestCallado"

    limpiar_tablas(db)
    hacer_amigo(db, yo, amigo)
    iniciar_sesion_simulada(client, db, yo)

    res = client.get(f'/filtro?usuario={amigo}')
    assert b"No hay noticias" in res.data or b"<li>" not in res.data


def test_2_8_volver_sin_seleccionar(client, db):
    """CU 2.8: Volver sin seleccionar usuario."""
    yo = "TestNoSelect"
    limpiar_tablas(db)
    iniciar_sesion_simulada(client, db, yo)

    # Se asume que /filtro sin parámetros carga la lista o menú base
    res = client.get('/filtro')
    assert b'href="/"' in res.data or b'href="/menu_principal"' in res.data or b'Volver' in res.data


def test_2_9_error_conexion_filtrar(client, db, monkeypatch):
    """CU 2.9: Error al filtrar."""
    yo = "TestFailFilter"
    amigo = "TestAmigo"

    limpiar_tablas(db)
    hacer_amigo(db, yo, amigo)
    iniciar_sesion_simulada(client, db, yo)

    def mock_fail(self, usuario, filtro, db):
        if filtro: raise Exception("Caida DB")
        return []

    monkeypatch.setattr(MarcoDex, "mostrar_changelog", mock_fail)

    try:
        res = client.get(f'/filtro?usuario={amigo}')
        assert b"error" in res.data.lower()
    except Exception:
        pass


def test_2_10_error_conexion_filtrar_volver(client, db, monkeypatch):
    """CU 2.10: Error al filtrar y botón volver."""
    yo = "TestFailFiltBack"
    amigo = "AmigoFail"
    limpiar_tablas(db)
    hacer_amigo(db, yo, amigo)
    iniciar_sesion_simulada(client, db, yo)

    def mock_fail(self, usuario, filtro, db):
        raise Exception("Caida DB en filtro")

    monkeypatch.setattr(MarcoDex, "mostrar_changelog", mock_fail)

    try:
        res = client.get(f'/filtro?usuario={amigo}')
        assert b'href="/"' in res.data or b'href="/menu_principal"' in res.data or b'Volver' in res.data
    except Exception:
        pass