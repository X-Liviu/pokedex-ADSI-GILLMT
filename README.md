# MarcoDex #
### Introducción ###
Este `README.md` es una guía sobre qué tiene el usuario para usar el programa.

### Dependencias ###
Requiere usar **Python 3.12**, además de las dependencias que se encuentran en `requirements.txt`:
```
pyTelegramBotAPI==4.29.1
pokebase==1.4.1
flask==3.1.
pytest==9.0.2
```
También se utiliza **sqlite3**, que viene por defecto con el intérprete.
### Instalación ###
La forma más sencilla de instalar los módulos de Python es mediante
```bash
python -m pip install -r requirements.txt
```
Donde `python` es el nombre del ejecutable.

### Casos de Prueba (Test) ###
Al lado de la carpeta `app` se encuentra el directorio `test`, donde se
realizan todos los casos de prueba de cada caso de uso. Un caso de uso
está asocieado con un archivo `.py` de test. Antes de realizar los tests
es recomendable leer el siguiente **inciso**:
> Los archivos `.py` de test que se encuentren en el directorio
> `test/test_usando_conftest` usan una base de datos sqlite diferente
> a la que usa app que se llama `dbtest.sqlite` y están en `root`, al lado
> de `app` y `test`. Antes de ejecutar un test.py que esté en
> `test_usando_conftest`, borra `dbtest.sqlite`.

### Glosario ###
- Python: https://python.org
- pyTelegramBotAPI: https://github.com/eternnoir/pyTelegramBotAPI
- Flask: https://flask.palletsprojects.com/en/stable/
- SQLite: https://sqlite.org/
- sqlite3: https://docs.python.org/3/library/sqlite3.html
- pytest: https://docs.pytest.org/en/stable/