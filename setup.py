import os

def instalar_dependencias(p_path: str, p_requeriments: str) -> None:
    os.system(f'{p_path}\\pip install -r {p_requeriments}')

def main() -> None:
    # Se da por hecho que es Windows
    ruta_python: str = ".venv\\Scripts"
    ruta_actual: str = f"{os.getcwd()}"
    mis_requisitos: str = f"{ruta_actual}\\requeriments.txt"
    instalar_dependencias(ruta_python, mis_requisitos )

if __name__ == '__main__':
    main()