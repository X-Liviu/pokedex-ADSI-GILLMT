from app.controller.model.prueba_nombre_aleatorio import generar_nombre

def get_pokemon(cant: int):
    return [ generar_nombre() for indice in range(cant) ]

def get_nombres(cant: int):
    return [ generar_nombre() for indice in range(cant) ]