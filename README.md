
<h1 align="center">Liviu y sus Marcos</h1>
---
<p align="center">
  <img src="app/static/imagenes/logo.png" alt="Logo del Proyecto" width="200">
</p>

### 📋 Sobre el Proyecto
Este documento sirve como guía técnica y de usuario para la instalación, configuración y despliegue del programa. El sistema integra **Pokebase** para gestión de datos Pokémon y **pyTelegramBotAPI** para la interacción vía bot.

### ⚙️ Requisitos y Dependencias

El proyecto está construido sobre **Python 3.12**. Las librerías principales son:

* **Flask (3.1.2):** Framework web.
* **pyTelegramBotAPI (4.29.1):** Interfaz para el Bot de Telegram.
* **Pokebase (1.4.1):** Wrapper de la API de Pokémon.
* **Pytest (9.0.2):** Suite de pruebas.
* **SQLite3:** Base de datos (incluida en Python).

### 🚀 Instalación

Sigue estos pasos para poner en marcha el entorno:

1.  **Clonar el repositorio y situarse en la raíz.**
2.  **Crear un entorno virtual (opcional pero recomendado):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Linux/Mac
    .venv\Scripts\activate     # En Windows
    ```
3.  **Instalar dependencias:**
    ```bash
    python -m pip install -r requirements.txt
    ```

### 🧪 Casos de Prueba (Testing)

Las pruebas unitarias y de integración se encuentran en el directorio `test/`. Cada caso de uso está asociado a un archivo `.py` específico.

#### ⚠️ Nota Importante sobre la Base de Datos de Test

> **Atención:** Los tests ubicados en `test/test_usando_conftest` utilizan una base de datos aislada llamada `dbtest.sqlite` (ubicada en la raíz).
>
> **Antes de ejecutar estos tests, debes borrar manualmente el archivo `dbtest.sqlite`**. Debido a esto, las pruebas van a tardar más tiempo debido a la recreación de tablas e inserción de pokemons usando la API de pokebase..

#### Ejecución de pruebas
Para lanzar las pruebas completas desde la terminal (estando en la raíz del proyecto):

```bash
python -m pytest tests/