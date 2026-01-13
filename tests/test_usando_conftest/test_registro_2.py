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


@pytest.mark.parametrize("campo_vacio", ['nombre', 'apellido', 'correo', 'usuario', 'contrasena', 'contrasena_rep'])
def test_1_4_a_1_7_registro_campos_vacios(client, campo_vacio):
    """
    CU: Registrarse (1.4 - 1.7)
    El registro se realiza dejando algún campo vacío.
    Resultado esperado: Salta un aviso de validación (Flash message).
    """
    # Datos base completos
    datos = {
        'nombre': 'Test',
        'apellido': 'Test',
        'correo': 't@t.com',
        'usuario': 'UserTest',
        'contrasena': '123',
        'contrasena_rep': '123'
    }

    # Vaciamos el campo que toca en esta iteración del test
    datos[campo_vacio] = ''

    # Ejecutamos la petición
    respuesta = client.post('/registrarse', data=datos, follow_redirects=True)

    # Verificamos que salta TU nuevo mensaje de seguridad
    # Nota: Usamos la codificación correcta para las tildes si fuera necesario,
    # pero tu mensaje "vacíos" usa í (utf-8: \xc3\xad)
    assert b"Error: No es posible con campos vac\xc3\xados." in respuesta.data
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