import pytest
from app.controller.model.gestorUsuario_controller import gestorUsuario #Necesario para poder borrar objetos en memoria para probar que la BD falla en el test 2.10

#TESTS DE LIVIU
def test_2_1_login_exitoso(client):
    """
    CU: Iniciar sesión (2.1)
    Datos correctos.
    Resultado esperado: Redirige a página principal.
    """
    # AshKetchum / 1234 existen en schema.sql
    datos_login = {
        'usuario': 'AshKetchum',
        'contrasena': '1234'
    }

    respuesta = client.post('/identificacion', data=datos_login, follow_redirects=True)

    # Verificar redirección exitosa (status 200 tras redirect)
    assert respuesta.status_code == 200

    # Verificar sesión creada
    with client.session_transaction() as sess:
        assert sess['usuario'] == 'AshKetchum'
        assert sess['rol'] == 'VERIF'  # Ash es VERIF en el schema


def test_2_2_login_usuario_vacio(client):
    """
    CU: Iniciar sesión (2.2)
    Campo usuario vacío.
    Resultado esperado: Aviso de usuario vacío (o incorrecto).
    """
    datos_login = {
        'usuario': '',
        'contrasena': '1234'
    }
    respuesta = client.post('/identificacion', data=datos_login, follow_redirects=True)

    # El controlador actual probablemente flash "Usuario o contraseña incorrectos"
    # al no encontrar al usuario vacío en la BD.
    assert b"Usuario o contrase\xc3\xb1a incorrectos" in respuesta.data


def test_2_3_login_contrasena_vacia(client):
    """
    CU: Iniciar sesión (2.3)
    Campo contraseña vacía.
    Resultado esperado: Aviso de contraseña vacía (o incorrecto).
    """
    datos_login = {
        'usuario': 'AshKetchum',
        'contrasena': ''
    }
    respuesta = client.post('/identificacion', data=datos_login, follow_redirects=True)

    assert b"Usuario o contrase\xc3\xb1a incorrectos" in respuesta.data


def test_2_4_login_usuario_incorrecto_contra_correcta(client):
    """
    CU: Iniciar sesión (2.4)
    Usuario incorrecto, contraseña correcta (para otro usuario o genérica).
    Resultado esperado: Aviso incorrecto.
    """
    datos_login = {
        'usuario': 'UsuarioInexistente',
        'contrasena': '1234'
    }
    respuesta = client.post('/identificacion', data=datos_login, follow_redirects=True)

    assert b"Usuario o contrase\xc3\xb1a incorrectos" in respuesta.data
    # Asegurar que NO se inició sesión
    with client.session_transaction() as sess:
        assert 'usuario' not in sess


def test_2_5_login_usuario_correcto_contra_incorrecta(client):
    """
    CU: Iniciar sesión (2.5)
    Usuario correcto, contraseña incorrecta.
    Resultado esperado: Aviso incorrecto.
    """
    datos_login = {
        'usuario': 'AshKetchum',
        'contrasena': 'ClaveErronea'
    }
    respuesta = client.post('/identificacion', data=datos_login, follow_redirects=True)

    assert b"Usuario o contrase\xc3\xb1a incorrectos" in respuesta.data


def test_2_6_login_ambos_incorrectos(client):
    """
    CU: Iniciar sesión (2.6)
    Ambos incorrectos.
    Resultado esperado: Aviso incorrecto.
    """
    datos_login = {
        'usuario': 'Nadie',
        'contrasena': 'Nada'
    }
    respuesta = client.post('/identificacion', data=datos_login, follow_redirects=True)

    assert b"Usuario o contrase\xc3\xb1a incorrectos" in respuesta.data


def test_2_7_login_espacios_usuario(client):
    """
    CU: Iniciar sesión (2.7)
    Espacios al principio o final del nombre de usuario.
    Resultado esperado: Aviso incorrecto (el sistema no debe hacer trim automático según el PDF).
    """
    # ' AshKetchum ' no es igual a 'AshKetchum'
    datos_login = {
        'usuario': ' AshKetchum ',
        'contrasena': '1234'
    }
    respuesta = client.post('/identificacion', data=datos_login, follow_redirects=True)

    # Según PDF: "El sistema da un aviso de que el usuario... son incorrectos"
    assert b"Usuario o contrase\xc3\xb1a incorrectos" in respuesta.data


def test_2_8_login_espacios_contrasena(client):
    """
    CU: Iniciar sesión (2.8)
    Espacios al principio o final de la contraseña.
    Resultado esperado: Aviso incorrecto.
    """
    datos_login = {
        'usuario': 'AshKetchum',
        'contrasena': ' 1234 '
    }
    respuesta = client.post('/identificacion', data=datos_login, follow_redirects=True)

    assert b"Usuario o contrase\xc3\xb1a incorrectos" in respuesta.data


def test_2_10_login_bd_caida(client, monkeypatch):
    """
    CU: Iniciar sesión (2.10) - Simulación de fallo crítico
    """

    # 1. Definimos el fallo simulado
    def mock_iniciar_sesion_fallido(*args, **kwargs):
        raise Exception("Simulación: Base de datos caída / Error Técnico")

    # 2. Parcheamos directamente el método 'iniciarSesion' del GESTOR.
    # Esto intercepta la llamada antes de que toque la BD o la caché.
    monkeypatch.setattr(gestorUsuario, "iniciarSesion", mock_iniciar_sesion_fallido)

    datos_login = {
        'usuario': 'AshKetchum',
        'contrasena': '1234'
    }

    # 3. Ejecutamos la petición
    respuesta = client.post('/identificacion', data=datos_login, follow_redirects=True)

    # 4. Verificamos que el controlador capturó la excepción y mostró el mensaje
    assert b"Error t\xc3\xa9cnico o de conexi\xc3\xb3n" in respuesta.data