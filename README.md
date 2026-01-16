<h1 align="center">Liviu y sus Marcos</h1>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12-blue.svg" alt="Python 3.12">
  <img src="https://img.shields.io/badge/flask-3.1.2-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/testing-pytest-yellow.svg" alt="Pytest">
  <img src="https://img.shields.io/badge/status-active-success.svg" alt="Status">
</p>

<p align="center">
  <img src="app/static/imagenes/logo.png" alt="Logo del Proyecto" width="200">
</p>

---

### 📋 Sobre el Proyecto

Este documento sirve como guía técnica y de usuario para la instalación, configuración y despliegue del sistema **Liviu y sus Marcos**.

La aplicación integra la potencia de **Pokebase** para la gestión exhaustiva de datos Pokémon y utiliza **pyTelegramBotAPI** para facilitar una interacción fluida y automatizada a través de un Bot de Telegram.

### ⚙️ Requisitos y Dependencias

El proyecto está construido sobre **Python 3.12**. Las librerías y tecnologías principales son:

| Tecnología | Versión | Descripción |
| :--- | :--- | :--- |
| **Flask** | 3.1.2 | Framework web para el backend. |
| **pyTelegramBotAPI** | 4.29.1 | Interfaz de comunicación con Telegram. |
| **Pokebase** | 1.4.1 | Wrapper para el consumo de la API de Pokémon. |
| **Pytest** | 9.0.2 | Suite para pruebas unitarias y de integración. |
| **SQLite3** | N/A | Base de datos ligera (nativa en Python). |

### 🚀 Instalación y Despliegue

Sigue estos pasos para configurar el entorno de desarrollo:

1.  **Clonar el repositorio:**
    Sitúate en la raíz del proyecto tras la descarga.

2.  **Configurar el entorno virtual (Recomendado):**
    ```bash
    python -m venv .venv
    
    # Activación:
    source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate     # Windows
    ```

3.  **Instalar dependencias:**
    ```bash
    python -m pip install -r requirements.txt
    ```

### ⚡ Consideraciones de Rendimiento

> **Nota sobre la Precarga de Datos:**
> Para optimizar los tiempos de espera durante el despliegue inicial y la ejecución de las pruebas, el sistema está configurado para realizar la **precarga únicamente de los 15 primeros equipos Pokémon** desde la API.
>
> Esta decisión de diseño evita que la primera ejecución y los tests tarden en exceso debido a la latencia de red, garantizando un entorno de desarrollo ágil sin sacrificar la funcionalidad principal.

### 🧪 Casos de Prueba (Testing)

Las pruebas unitarias y de integración se encuentran en el directorio `tests/`.

#### ⚠️ Gestión de la Base de Datos de Test

Los tests ubicados en `tests/test_usando_conftest` utilizan una base de datos aislada llamada `dbtest.sqlite` que se genera en la raíz.

> **❗ IMPORTANTE:** > Antes de ejecutar estos tests, **debes borrar manualmente el archivo `dbtest.sqlite`** si existe.
>
> Al borrarla, el sistema recreará las tablas e insertará los datos nuevamente usando la API de Pokebase. Ten en cuenta que, aunque esté limitada a 15 equipos tanto la creación de la base de datos de tests como la de la propia aplicación, esta operación puede tomar unos instantes.

#### Ejecución de pruebas

Para lanzar la suite completa de pruebas, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
python -m pytest tests/