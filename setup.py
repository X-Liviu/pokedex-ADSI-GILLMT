import os
def instalar_dependencias_windows(p_path: str, p_requirements: str) -> None:
    os.system(f'{p_path}\\pip install -r {p_requirements}')

def instalar_dependencias_posix(p_path: str, p_requiriments: str) -> None:
    os.system(f'{p_path}/pip install -r {p_requiriments}')

def main() -> None:
    ruta_actual: str = f"{os.getcwd()}"
    nombre_archivo_requirements: str = "requirements.txt"

    if os.name == 'nt':
        ruta_python: str = ".venv\\Scripts"
        mis_requisitos: str = f"{ruta_actual}\\{nombre_archivo_requirements}"
        instalar_dependencias_windows(ruta_python, mis_requisitos)
    elif os.name == 'posix':
        ruta_python: str = ".venv/Scripts"
        mis_requisitos: str = f"{ruta_actual}/{nombre_archivo_requirements}"
        instalar_dependencias_posix(ruta_python, mis_requisitos)

if __name__ == '__main__':
    main()