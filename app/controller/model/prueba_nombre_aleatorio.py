from app.custom_types import Custom_types
from random import randint, uniform

def get_abecedario() -> str:
    resultado: str = ""
    codigo_primera_letra = 65
    codigo_ultima_letra = 91
    for indice_letra in range(codigo_primera_letra, codigo_ultima_letra):
        resultado += chr(indice_letra)

    return resultado

def generar_nombre_por_cantidad_letras(cant_letras: int) -> str:
    resultado: str = ""
    abecedario: str = get_abecedario()
    longitud: int = len(abecedario)

    cantidad: int = 0
    while cantidad < cant_letras:
        indice_aleatorio: int = randint(0, longitud - 1)
        resultado += abecedario[indice_aleatorio]
        cantidad += 1

    return resultado

def generar_nombre() -> str:
    cantidad_letras: int = randint(3, 10)
    return generar_nombre_por_cantidad_letras(cantidad_letras)

def generar_rareza() -> float:
    return uniform(1, 7)

def prueba_ranking(cantidad: int) -> Custom_types.Ranking.Usuarios:
    resultado: Custom_types.Ranking.Usuarios = {"usuarios": []}

    ultimo_puesto: int = cantidad + 1

    for indice_usuario in range(1, ultimo_puesto):
        usuario_actual = {
            "nombre": generar_nombre(),
            "rareza": generar_rareza(),
            "puesto": indice_usuario
        }

        resultado.get("usuarios").append(usuario_actual)

    return resultado