import pytest
from flask import session

#TESTS DE LIVIU
def test_1_1_registro_exitoso(client):
    """
    CU: Registrarse (1.1)
    El registro de usuario se realiza con datos correctos.
    Resultado esperado: Se crea usuario y redirige al inicio (login automático).
    """
    datos_registro = {
        'nombre': 'Nuevo',
        'apellido': 'Usuario',
        'correo': 'nuevo@test.com',
        'usuario': 'NuevoUser123',
        'contrasena': 'password123',
        'contrasena_rep': 'password123'
    }

    # Enviamos POST
    respuesta = client.post('/registrarse', data=datos_registro, follow_redirects=True)

    # Verificaciones
    # 1. Debe redirigir al index (Status 200 tras redirect)
    assert respuesta.status_code == 200

    # 2. Comprobamos que en la sesión se ha guardado el usuario
    with client.session_transaction() as sess:
        assert sess['usuario'] == 'NuevoUser123'


def test_1_2_registro_correo_duplicado(client):
    """
    CU: Registrarse (1.2)
    Correo ya registrado.
    [cite_start]Resultado esperado: Aviso de correo registrado[cite: 3].
    """
    # 'ash@pueblopaleta.com' ya existe en los datos semilla
    datos_registro = {
        'nombre': 'Otro',
        'apellido': 'Ash',
        'correo': 'ash@pueblopaleta.com',
        'usuario': 'UsuarioUnico123',
        'contrasena': '1234',
        'contrasena_rep': '1234'
    }

    respuesta = client.post('/registrarse', data=datos_registro, follow_redirects=True)

    # Tu controlador devuelve flash("Error: El nombre de usuario o el correo ya están en uso.")
    assert b"Error: El nombre de usuario o el correo ya est\xc3\xa1n en uso." in respuesta.data


def test_1_3_registro_usuario_duplicado(client):
    """
    CU: Registrarse (1.3)
    Nombre de usuario ya registrado.
    [cite_start]Resultado esperado: Aviso de usuario registrado[cite: 3].
    """
    # 'AshKetchum' ya existe en los datos semilla
    datos_registro = {
        'nombre': 'Impostor',
        'apellido': 'Ketchum',
        'correo': 'impostor@kanto.com',
        'usuario': 'AshKetchum',
        'contrasena': '1234',
        'contrasena_rep': '1234'
    }

    respuesta = client.post('/registrarse', data=datos_registro, follow_redirects=True)

    assert b"Error: El nombre de usuario o el correo ya est\xc3\xa1n en uso." in respuesta.data


def test_1_8_registro_contrasenas_diferentes(client):
    """
    CU: Registrarse (1.8)
    Contraseñas diferentes en ambos campos.
    [cite_start]Resultado esperado: Aviso de contraseñas diferentes[cite: 3].
    """
    datos_registro = {
        'nombre': 'Test',
        'apellido': 'Test',
        'correo': 'test@pass.com',
        'usuario': 'PassTestUser',
        'contrasena': '1234',
        'contrasena_rep': '5678'  # Diferente
    }

    respuesta = client.post('/registrarse', data=datos_registro, follow_redirects=True)

    # Tu controlador actual valida esto llamando al modelo, que devuelve -1
    assert b"Error: Las contrase\xc3\xb1as no coinciden." in respuesta.data