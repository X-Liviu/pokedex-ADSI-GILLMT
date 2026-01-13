def test_ranking(client):
    """
    Vamos a iniciar sesion con GaryOak,
    que no es amigo de nadie y aparece en el ranking
    """
    client.post("/identificacion",
                data={"usuario": "GaryOak", "contrasena": "1234"}
                )

    """
    Antes de entrar a una pagina que requiera sesion es necesario
    iniciar sesion. La linea de arriba se encarga de ello
    """

    respuesta = client.get("/perfil_usuario/GaryOak")

    print(respuesta.data)

