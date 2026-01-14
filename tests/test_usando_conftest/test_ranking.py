from typing import Tuple

def iniciar_sesion(p_cliente, pNombreUsuario: str):
    """
    Muestra el ranking de usuarios
    con los pokemon mas raros.
    """
    respuesta = p_cliente.post("/identificacion",
                              data={"usuario": pNombreUsuario, "contrasena": "1234"},
                              follow_redirects=True
                              )

    """
    Antes de entrar a una pagina que requiera sesion es necesario
    iniciar sesion. La linea de arriba se encarga de ello
    """

    assert respuesta.status_code == 200


def test_ranking_1_1(client):
    """ 
    CASO 1.1: Usuario pulsa la opcion ”Ranking” en el menu
    principal y hay m´ınimo un usuario que tiene
    minimo un equipo.
    
    Resultado: Muestra el ranking de usuarios
    con los pokemon m´as raros.
    """

    iniciar_sesion(client, "GaryOak")

    respuesta = client.get("/ranking")

    assert respuesta.status_code == 200

    """
    En la base de datos original, AshKetchum es el primero
    y GaryOak el segundo. No hay mas usuarios con equipos
    """
    assert b"AshKetchum" in respuesta.data
    assert b"GaryOak" in respuesta.data

def test_ranking_2(client):
    """
    CASO 2: Usuario pulsa la opcion "Volver" en la
    pantalla del Ranking.

    Resultado: Devuelve al usuario al men´u
    principal.
    """

    iniciar_sesion(client, "GaryOak")

    respuesta = client.get("/ranking")

    assert respuesta.status_code == 200

    # Buscamos aquella linea en el html que dirija al menu princiàl y se llame la opcion volver
    objetivo: bytes = b"<a href=\"/\" class=\"boton-volver-estilo\">Volver</a>"

    assert objetivo in respuesta.data

    # Nos dirigimos de forma manual a "/" y comprobamos que sea el menu principal

    respuesta = client.get("/")

    assert respuesta.status_code == 200

    titulo: bytes = b"<title>Marcodex - Men\xc3\xba Principal</title>"

    assert titulo in respuesta.data

def perfil_usuario(p_respuesta, pNombreUsuario: str, pPuesto: int):
    etiquetas: Tuple[bytes, bytes, bytes, bytes] = (
        b"<img src=\"/static/imagenes/foto_perfil.svg\" class=\"foto-perfil-principal\" alt=\"Foto\">", # foto de perfil
        f"<div class=\"nombre-valor\">{pNombreUsuario}</div>".encode(),  # Nombre del usuario
        f"<span class=\"top-ranking\">#{pPuesto}</span>".encode(),  # Posicion en el ranking
        b"<div class=\"lista-pokemon\">",  # Equipo Pokemon
    )

    todo_correcto: bool = True
    indice: int = 0
    longitud: int = len(etiquetas)

    while (indice < longitud) and todo_correcto:
        todo_correcto = etiquetas[indice] in p_respuesta.data
        indice += 1

    assert todo_correcto

def test_ranking_3_1(client):
    """
    CASO 3.1: Usuario presiona un perfil con el que ya es
    amigo.

    Resultado: Aparece el perfil completo del
    usuario, incluyendo foto de per-
    fil, nombre de usuario, posicion
    en el ranking mundial y los
    pokemon de su equipo principal.
    """

    iniciar_sesion(client, "LiviuX")

    # LiviuX si es amigo de Ash
    respuesta = client.get("/perfil_usuario/AshKetchum")
    assert respuesta.status_code == 200

    perfil_usuario(respuesta, "AshKetchum", 1)

    # Ahora hay que comprobar que si son amigos
    etiqueta_si_es_amigo: bytes = b"<a class=\"estado-amigo\">Ya es tu amigo</a>"
    assert etiqueta_si_es_amigo in respuesta.data

def test_ranking_3_2(client):
    """
    CASO 3.2: Usuario presiona un perfil que no es su amigo.

    Resultado: Aparece el perfil completo del
    usuario, incluyendo foto de per-
    fil, nombre de usuario, posicion
    en el ranking mundial, los
    pokemon de su equipo principal
    y boton de ainadir amigo.
    """
    iniciar_sesion(client, "GorkaX")

    # GorkaX no es amigo de Gary
    respuesta = client.get("/perfil_usuario/GaryOak")
    assert respuesta.status_code == 200

    perfil_usuario(respuesta, "GaryOak", 2)

    # Ahora hay que comprobar que no son amigos
    etiqueta_no_es_amigo: bytes = b"<input type=\"submit\" name=\"submit_button\" value=\"Solicitud amistad\" class=\"btn-solicitud\">"
    assert etiqueta_no_es_amigo in respuesta.data

def test_ranking_3_3(client):
    """
    CASO 3.3: Usuario presiona su propio perfil.

    Resultado: Aparece su perfil completo, in-
    cluyendo foto de perfil, nombre
    de usuario, posicion en el rank-
    ing mundial, y los pokemon de
    su equipo principal.
    """

    iniciar_sesion(client, "GaryOak")

    respuesta = client.get("/perfil_usuario/GaryOak")
    assert respuesta.status_code == 200

    perfil_usuario(respuesta, "GaryOak", 2)

    # Ahora hay que comprobar que son la misma persona
    etiqueta_mismo_usuario: bytes = b"<a class=\"estado-amigo\">Eres t\xc3\xba</a>"
    assert etiqueta_mismo_usuario in respuesta.data

def test_ranking_4(client):
    """
    CASO 4: Usuario pulsa "ainadir amigo”

    Resultado: El usuario se ainade a su lista
    de amigos y ya no le aparece el
    boton de ainadir amigo..
    """

    iniciar_sesion(client, "GaryOak")

    # Gary no es amigo de nadie

    respuesta = client.get("/perfil_usuario/AshKetchum")
    assert respuesta.status_code == 200

    perfil_usuario(respuesta, "AshKetchum", 1)

    # Comprobamos que no son amigos
    etiqueta_no_es_amigo: bytes = b"<input type=\"submit\" name=\"submit_button\" value=\"Solicitud amistad\" class=\"btn-solicitud\">"
    assert etiqueta_no_es_amigo in respuesta.data

    respuesta = client.post(
        "/perfil_usuario/AshKetchum",
        data={"submit_button": "Solicitud amistad"},
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    # Comprobamos que es la misma pagina web
    perfil_usuario(respuesta, "AshKetchum", 1)

    # Comprobamos que si son amigos
    etiqueta_si_es_amigo: bytes = b"<a class=\"estado-amigo\">Ya es tu amigo</a>"
    assert etiqueta_si_es_amigo in respuesta.data

def test_ranking_5(client):
    """
    CASO 5.5: Usuario pulsa la opcion "Volver" en la
    pantalla del Perfil que ha seleccionado

    Resultado: Devuelve al usuario a la pantalla
    del Ranking.
    """

    iniciar_sesion(client, "GaryOak")

    respuesta = client.get("/perfil_usuario/AshKetchum")
    assert respuesta.status_code == 200

    # Buscamos aquella linea en el html que dirija al menu princiàl y se llame la opcion volver
    objetivo: bytes = b"<a href=\"/ranking\" class=\"boton-volver-estilo\">Volver</a>"
    assert objetivo in respuesta.data

    # Nos dirigimos de forma manual a "/ranking" y comprobamos que sea el menu principal

    respuesta = client.get("/ranking")

    assert respuesta.status_code == 200

    titulo: bytes = b"<title>Ranking Usuarios</title>"

    assert titulo in respuesta.data

"""
Este caso no sigue el orden porque modifica la base de datos. Si estuviera arriba
los las funciones test que estuvieran debajo no funcionarian, que no significa que
funcionen mal.
"""
def test_ranking_1_2(client):
    """
    CASO 1.2: Usuario pulsa la opcion "Ranking" en el menu
    principal y no hay ningun usuario que tenga
    equipos.

    Resultado: El sistema muestra el ranking
    vacio
    """

    iniciar_sesion(client, "GaryOak")

    # Vamos a eliminar los usuarios que tenian algun equipo en la BD
    # Obtenemos una conexión manual para limpiar la tabla antes del GET
    from conftest import Connection
    db = Connection()
    db.delete("DELETE FROM PokemonEnEquipo")
    db.delete("DELETE FROM Equipo")
    # Nota: No hace falta borrar usuarios, sin equipos no aparecen en el ranking

    respuesta = client.get("/ranking")
    assert respuesta.status_code == 200

    # Verificamos que los usuarios que antes estaban ya no aparecen
    assert b"AshKetchum" not in respuesta.data
    assert b"GaryOak" not in respuesta.data

    db.close()