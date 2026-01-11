--- LIMPIEZA INICIAL (Borra todo para empezar de cero y evitar errores) ---
DROP TABLE IF EXISTS EfectoTipo;
DROP TABLE IF EXISTS EspecieTipo;
DROP TABLE IF EXISTS PuedeUtilizar;
DROP TABLE IF EXISTS AtaquePokemon;
DROP TABLE IF EXISTS PokemonEnEquipo;
DROP TABLE IF EXISTS Publica;
DROP TABLE IF EXISTS AmigoDe;
DROP TABLE IF EXISTS OpcionChatbot;
DROP TABLE IF EXISTS Equipo;
DROP TABLE IF EXISTS Pokemon;
DROP TABLE IF EXISTS Ataques;
DROP TABLE IF EXISTS Tipo;
DROP TABLE IF EXISTS EspeciePokemon;
DROP TABLE IF EXISTS Pokedex;
DROP TABLE IF EXISTS Usuario;

--- CREACIÓN DE TABLAS ---

-- 1. Tabla: Usuario (CON LA RESTRICCIÓN CHECK)
CREATE TABLE Usuario (
    NombreUsuario TEXT PRIMARY KEY,
    Nombre TEXT,
    Apellido TEXT,
    Correo TEXT,
    Contrasena TEXT,
    Rol TEXT CHECK(Rol IN ('VERIF', 'NOVERIF', 'ADMIN'))
);

-- 2. Tabla: Pokédex (Región)
CREATE TABLE Pokedex (
    Region TEXT PRIMARY KEY,
    Generacion TEXT
);

-- 3. Tabla: Especie Pokémon
CREATE TABLE EspeciePokemon (
    Nombre TEXT PRIMARY KEY,
    Descripcion TEXT,
    Legendario BOOLEAN,
    AlturaMedia REAL,
    PesoMedia REAL,
    Region TEXT,
    FOREIGN KEY (Region) REFERENCES Pokedex(Region)
);

-- 4. Tabla: Tipo
CREATE TABLE Tipo (
    Nombre TEXT PRIMARY KEY,
    Descripcion TEXT
);

-- 5. Tabla: Ataques
CREATE TABLE Ataques (
    Nombre TEXT PRIMARY KEY,
    Dano INTEGER,
    EfectoSecundario TEXT,
    Precision INTEGER,
    NombreTipo TEXT,
    FOREIGN KEY (NombreTipo) REFERENCES Tipo(Nombre)
);

-- 6. Tabla: Pokémon (Instancia individual capturada)
CREATE TABLE Pokemon (
    idPokemon INTEGER PRIMARY KEY AUTOINCREMENT,
    numPokemon INTEGER,
    NombreCustom TEXT,
    Rareza INT,
    Shiny BOOLEAN,
    Altura REAL,
    Peso REAL,
    NombreEspecie TEXT,
    Imagen TEXT,
    FOREIGN KEY (NombreEspecie) REFERENCES EspeciePokemon(Nombre)
);

-- 7. Tabla: Equipo
CREATE TABLE Equipo (
    idEquipo INTEGER PRIMARY KEY AUTOINCREMENT,
    numEquipo INTEGER,
    NombreUsuario TEXT,
    FOREIGN KEY (NombreUsuario) REFERENCES Usuario(NombreUsuario)
);

-- 8. Tabla: Opción Chatbot
CREATE TABLE OpcionChatbot (
    Opcion TEXT PRIMARY KEY,
    Descripcion TEXT
);

--- TABLAS DE RELACIÓN (Muchos a Muchos) ---

-- 9. Amigo de
CREATE TABLE AmigoDe (
    NombreUsuario1 TEXT,
    NombreUsuario2 TEXT,
    PRIMARY KEY (NombreUsuario1, NombreUsuario2),
    FOREIGN KEY (NombreUsuario1) REFERENCES Usuario(NombreUsuario),
    FOREIGN KEY (NombreUsuario2) REFERENCES Usuario(NombreUsuario)
);

-- 10. Publica
CREATE TABLE Publica (
    NombreUsuario TEXT,
    FechaHora DATETIME,
    Contenido TEXT,
    PRIMARY KEY (NombreUsuario, FechaHora),
    FOREIGN KEY (NombreUsuario) REFERENCES Usuario(NombreUsuario)
);

-- 11. PokemonEnEquipo
CREATE TABLE PokemonEnEquipo (
    idEquipoInterno INTEGER,
    idPokemon INTEGER,
    PRIMARY KEY (idEquipoInterno, idPokemon),
    FOREIGN KEY (idEquipoInterno) REFERENCES Equipo(idEquipo), -- Corregido a idEquipo
    FOREIGN KEY (idPokemon) REFERENCES Pokemon(idPokemon)
);

-- 12. AtaquePokemon
CREATE TABLE AtaquePokemon (
    idPokemon INTEGER,
    nombreAtaque TEXT,
    PRIMARY KEY (idPokemon, nombreAtaque),
    FOREIGN KEY (idPokemon) REFERENCES Pokemon(idPokemon),
    FOREIGN KEY (nombreAtaque) REFERENCES Ataques(Nombre)
);

-- 13. PuedeUtilizar
CREATE TABLE PuedeUtilizar (
    NombreEspecie TEXT,
    NombreAtaque TEXT,
    PRIMARY KEY (NombreEspecie, NombreAtaque),
    FOREIGN KEY (NombreEspecie) REFERENCES EspeciePokemon(Nombre),
    FOREIGN KEY (NombreAtaque) REFERENCES Ataques(Nombre)
);

-- 14. EspecieTipo
CREATE TABLE EspecieTipo (
    NombreEspecie TEXT,
    NombreTipo TEXT,
    PRIMARY KEY (NombreEspecie, NombreTipo),
    FOREIGN KEY (NombreEspecie) REFERENCES EspeciePokemon(Nombre),
    FOREIGN KEY (NombreTipo) REFERENCES Tipo(Nombre)
);

-- 15. EfectoTipo
CREATE TABLE EfectoTipo (
    NombreTipo1 TEXT,
    NombreTipo2 TEXT,
    Efecto TEXT,
    PRIMARY KEY (NombreTipo1, NombreTipo2),
    FOREIGN KEY (NombreTipo1) REFERENCES Tipo(Nombre),
    FOREIGN KEY (NombreTipo2) REFERENCES Tipo(Nombre)
);


--- INSERTAR DATOS DE PRUEBA (Refactorizados) ---

-- A. Insertar Usuarios (Solo VERIF, ADMIN, NOVERIF)
INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol)
VALUES ('LiviuX', 'Liviu', 'Deleanu', 'ash@pueblopaleta.com', '1234', 'VERIF');

INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol)
VALUES ('TataX', 'Tabata', 'Morente', 'tata@kanto.net', '1234', 'VERIF');

INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol)
VALUES ('GorkaX', 'Gorka', 'Bidaguren', 'gorki@pokedex.org', '1234', 'ADMIN');

INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol)
VALUES ('LauraX', 'Laura', 'Calvo', 'laura@celeste.com', '1234', 'VERIF');

INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol)
VALUES ('MarcoX', 'Marco', 'Lartategui', 'marco@teamrocket.com', '1234', 'NOVERIF');


-- B. Datos necesarios para que los equipos funcionen (Región, Especie)
INSERT OR IGNORE INTO Pokedex VALUES ("Kanto", "Primera");
INSERT OR IGNORE INTO EspeciePokemon VALUES ("Pikachu", "Ratón eléctrico", FALSE, 0.4, 6.0, "Kanto");
INSERT OR IGNORE INTO EspeciePokemon VALUES ("Eevee", "Evolución", FALSE, 0.3, 6.5, "Kanto");

-- C. Pokémons individuales (Instancias)
-- Pikachu de Ash
INSERT OR IGNORE INTO Pokemon (idPokemon, NombreCustom, Rareza, Shiny, Altura, Peso, NombreEspecie, Imagen)
VALUES (1, "Pikachu", 5, FALSE, 0.4, 6.0, "Pikachu", "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png");

-- Eevee de Gary
INSERT OR IGNORE INTO Pokemon (idPokemon, NombreCustom, Rareza, Shiny, Altura, Peso, NombreEspecie, Imagen)
VALUES (2, "Eevee", 4, FALSE, 0.3, 6.5, "Eevee", "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/133.png");

-- D. Equipos (Vinculados a los nuevos usuarios Ash y Gary)
INSERT OR IGNORE INTO Equipo (idEquipo, numEquipo, NombreUsuario) VALUES (1, 1, "AshKetchum");
INSERT OR IGNORE INTO Equipo (idEquipo, numEquipo, NombreUsuario) VALUES (2, 1, "GaryOak");

-- E. Relación Pokemon - Equipo
INSERT OR IGNORE INTO PokemonEnEquipo (idEquipoInterno, idPokemon) VALUES (1, 1); -- Pikachu en equipo de Ash
INSERT OR IGNORE INTO PokemonEnEquipo (idEquipoInterno, idPokemon) VALUES (2, 2); -- Eevee en equipo de Gary