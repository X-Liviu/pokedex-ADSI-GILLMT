from typing import Tuple
from app.model.usuario_ranking import UsuarioRanking
from app.model.utils.custom_types import Custom_types

Testing = Custom_types.Testing

def test_es_mi_nombre() -> Tuple[int, str]:
    def mismo_nombre(usuario: UsuarioRanking) -> int:
        error: int = Testing.EsMiNombre.NO_ERROR
        nombre_actual: str = "prueba1"
        if not usuario.es_mi_nombre(nombre_actual):
            error = Testing.EsMiNombre.SAME_NAME_ERROR

        return error

    def diferente_nombre(usuario: UsuarioRanking) -> int:
        error: int = Testing.EsMiNombre.NO_ERROR
        nombre_actual: str = "distinto"
        if usuario.es_mi_nombre(nombre_actual):
            error = Testing.EsMiNombre.DIFFERENT_NAME_ERROR

        return error

    error: int = Testing.EsMiNombre.NO_ERROR

    usuario_actual = UsuarioRanking("prueba1", 0)

    # Caso 1: mismo nombre
    error = mismo_nombre(usuario_actual)
    caso: str = "1"

    if error == Testing.EsMiNombre.NO_ERROR:
        # Caso 2: diferente nombre
        error = diferente_nombre(usuario_actual)
        caso: str = "2"

    if error == Testing.EsMiNombre.NO_ERROR:
        caso = None

    return (error, caso)

def test_add_rareza() -> Tuple[int, str]:
    def check_addition(usuario: UsuarioRanking, cantidad: int) -> bool:
        valor_inicial: int = usuario.to_dict()["rareza"]
        usuario.add_rareza(cantidad)
        valor_esperado: int = valor_inicial + cantidad

        return valor_esperado == usuario.to_dict()["rareza"]

    def add_to_user(usuario: UsuarioRanking) -> int:
        error: int = Testing.AddRareza.NO_ERROR
        cantidad: int = 5

        if not check_addition(usuario, cantidad):
            error = Testing.AddRareza.ADDITION_ERROR

        return error

    def subtract_to_user(usuario: UsuarioRanking) -> int:
        error: int = Testing.AddRareza.NO_ERROR
        cantidad: int = -5

        if not check_addition(usuario, cantidad):
            error = Testing.AddRareza.SUBTRACTION_ERROR

        return error

    error: int = Testing.AddRareza.NO_ERROR

    # Caso 1: 0 de ranking
    usuario_actual: UsuarioRanking = UsuarioRanking("prueba2", 0)

    # Caso 1.1: Suma a un ranking 0
    error = add_to_user(usuario_actual)
    caso: str = "1.1"

    if error == Testing.AddRareza.NO_ERROR:
        # Caso 1.2: Resta a un ranking 0
        error = subtract_to_user(usuario_actual)
        caso = "1.2"

    # Caso 2: ranking positivo
    usuario_actual = UsuarioRanking("prueba2", 5)

    if error == Testing.AddRareza.NO_ERROR:
        # Caso 2.1: Suma a un ranking positivo
        error = add_to_user(usuario_actual)
        caso = "2.1"

    if error == Testing.AddRareza.NO_ERROR:
        # Caso 2.2: Resta a un ranking positivo
        error = subtract_to_user(usuario_actual)
        caso = "2.2"

    # Caso 3: Ranking negativo
    usuario_actual = UsuarioRanking("prueba2", -5)

    if error == Testing.AddRareza.NO_ERROR:
        # Caso 3.1: Suma a ranking negativo
        error = add_to_user(usuario_actual)
        caso = "3.1"

    if error == Testing.AddRareza.NO_ERROR:
        # Caso 3.2: Resta a ranking negativo
        error = subtract_to_user(usuario_actual)
        caso = "3.2"

    if error == Testing.AddRareza.NO_ERROR:
        caso = None

    return (error, caso)

def test_compare() -> Tuple[int, str]:
    def compare(usuario: UsuarioRanking, cantidad: int) -> int:
        valor_inicial: int = usuario.to_dict()["rareza"]
        usuario_actual: UsuarioRanking = UsuarioRanking("prueba3", cantidad + valor_inicial)
        return usuario.compare(usuario_actual)

    def compare_to_greater(usuario: UsuarioRanking) -> int:
        error: int = Testing.Compare.NO_ERROR
        cantidad: int = 5

        if compare(usuario, cantidad) != -1:
            error = Testing.Compare.GREATER_THAN_ERROR

        return error

    def compare_to_lower(usuario: UsuarioRanking) -> int:
        error: int = Testing.Compare.NO_ERROR
        cantidad: int = -5

        if compare(usuario, cantidad) != 1:
            error = Testing.Compare.LOWER_THAN_ERROR

        return error

    def compare_to_equal(usuario: UsuarioRanking) -> int:
        error: int = Testing.Compare.NO_ERROR
        cantidad: int = 0

        if compare(usuario, cantidad) != 0:
            error = Testing.Compare.EQUAL_TO_ERROR

        return error

    def compare_to_zero(usuario: UsuarioRanking) -> int:
        usuario_actual: UsuarioRanking = UsuarioRanking("prueba3", 0)
        return usuario.compare(usuario_actual)

    error: int = Testing.Compare.NO_ERROR

    # Caso 1: Uno de los usuarios tiene el ranking a 0
    usuario_actual: UsuarioRanking = UsuarioRanking("prueba3", 0)

    # Caso 1.1: Comparar uno de ranking 0 con uno de ranking positivo
    error = compare_to_greater(usuario_actual)
    caso: str = "1.1"

    if error == Testing.Compare.NO_ERROR:
        # Caso 1.2: Comparar de ranking 0 con uno de ranking negativo
        error = compare_to_lower(usuario_actual)
        caso = "1.2"

    if error == Testing.Compare.NO_ERROR:
        # Caso 1.3: Comparar uno de ranking 0 con otro de ranking 0
        error = compare_to_equal(usuario_actual)
        caso = "1.3"

    # Caso 2: Uno de los usuarios tiene el ranking positivo
    usuario_actual = UsuarioRanking("prueba3", 5)

    if error == Testing.Compare.NO_ERROR:
        # Caso 2.1: Comparar uno de ranking positivo con otro de ranking positivo mayor
        error = compare_to_greater(usuario_actual)
        caso = "2.1"

    if error == Testing.Compare.NO_ERROR:
        # Caso 2.2: Comparar uno de ranking positivo con otro de ranking positivo menor
        usuario_pequeno: UsuarioRanking = UsuarioRanking("prueba3", 4)
        caso = "2.2"

        if usuario_pequeno.compare(usuario_actual) != -1:
            error = Testing.Compare.LOWER_THAN_ERROR

    if error == Testing.Compare.NO_ERROR:
        # Caso 2.3: Comparar uno de ranking positivo con uno de ranking 0
        resultado: int = compare_to_zero(usuario_actual)
        caso = "2.3"
        if resultado != 1:
            error = Testing.Compare.GREATER_THAN_ERROR

    if error == Testing.Compare.NO_ERROR:
        # Caso 2.4: Comparar uno de ranking positivo con uno de ranking negativo
        usuario_negativo: UsuarioRanking = UsuarioRanking("prueba3", -5)
        caso = "2.4"
        if usuario_negativo.compare(usuario_actual) != -1:
            error = Testing.Compare.LOWER_THAN_ERROR

    if error == Testing.Compare.NO_ERROR:
        # Caso 2.5: Comparar uno de ranking con otro del mismo ranking
        caso = "2.5"
        error = compare_to_lower(usuario_actual)

    # Caso 3: Uno de los usuarios tiene el ranking negativo
    usuario_actual = UsuarioRanking("prueba3", -5)

    if error == Testing.Compare.NO_ERROR:
        # Caso 3.1: Comparar uno negativo con uno positivo
        usuario_positivo: UsuarioRanking = UsuarioRanking("prueba3", 5)
        caso = "3.1"
        if usuario_positivo.compare(usuario_actual) != 1:
            error = Testing.Compare.GREATER_THAN_ERROR

    if error == Testing.Compare.NO_ERROR:
        # Caso 3.2: Comparar uno negativo con otro de ranking 0
        caso = "3.2"
        resultado: int = compare_to_zero(usuario_actual)
        if resultado != -1:
            error = Testing.Compare.LOWER_THAN_ERROR

    if error == Testing.Compare.NO_ERROR:
        # Caso 3.3: Comparar uno negativo con otro negativo mayor
        caso = "3.3"
        usuario_mayor: UsuarioRanking = UsuarioRanking("prueba3", -4)

        if usuario_mayor.compare(usuario_actual) != 1:
            error = Testing.Compare.GREATER_THAN_ERROR

    if error == Testing.Compare.NO_ERROR:
        # Caso 3.4 Comparar uno negativo con otro negativo menor
        error = compare_to_lower(usuario_actual)
        caso = "3.4"

    if error == Testing.Compare.NO_ERROR:
        # Caso 3.5 Comparar uno negativo con uno igual que este
        error = compare_to_equal(usuario_actual)
        caso = "3.5"

    if error == Testing.Compare.NO_ERROR:
        caso = None

    return (error, caso)

def main() -> None:
    print("Casos de Prueba de Caja Negra de UsuarioRanking")

    print("Caso de Prueba del metodo es_mi_nombre:")
    resultado: Tuple[int, str] = test_es_mi_nombre()
    if resultado[0] == Testing.EsMiNombre.NO_ERROR:
        print("\tTodo correcto!")
    else:
        print(f"\tError de tipo {Testing.EsMiNombre.toString(resultado[1])} en el caso {resultado[0]}")

    print("Caso de Prueba del metodo add_rareza:")
    resultado: Tuple[int, str] = test_add_rareza()
    if resultado[0] == Testing.AddRareza.NO_ERROR:
        print("\tTodo correcto!")
    else:
        print(f"\tError de tipo {Testing.AddRareza.toString(resultado[1])} en el caso {resultado[0]}")

    print("Caso de Prueba del metodo compare:")
    resultado: Tuple[int, str] = test_compare()
    if resultado[0] == Testing.Compare.NO_ERROR:
        print("\tTodo correcto!")
    else:
        print(f"\tError de tipo {Testing.Compare.toString(resultado[1])} en el caso {resultado[0]}")

if __name__ == '__main__':
    main()