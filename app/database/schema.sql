-- 1. Tabla: Usuario
CREATE TABLE IF NOT EXISTS Usuario (
    NombreUsuario TEXT PRIMARY KEY,
    Nombre TEXT,
    Apellido TEXT,
    Correo TEXT,
    Contrasena TEXT,
    Rol TEXT,
    Verificado BOOLEAN
);

-- 2. Tabla: Pokédex (Región)
CREATE TABLE IF NOT EXISTS Pokedex (
    Region TEXT PRIMARY KEY,
    Generacion TEXT
);

-- 3. Tabla: Especie Pokémon
CREATE TABLE IF NOT EXISTS EspeciePokemon (
    Nombre TEXT PRIMARY KEY,
    Descripcion TEXT,
    Legendario BOOLEAN,
    AlturaMedia REAL,
    PesoMedia REAL,
    Region TEXT,
    FOREIGN KEY (Region) REFERENCES Pokedex(Region)
);

-- 4. Tabla: Tipo
CREATE TABLE IF NOT EXISTS Tipo (
    Nombre TEXT PRIMARY KEY,
    Descripcion TEXT
);

-- 5. Tabla: Ataques
CREATE TABLE IF NOT EXISTS Ataques (
    Nombre TEXT PRIMARY KEY,
    Dano INTEGER, -- TODO: DANO
    EfectoSecundario TEXT,
    Precision INTEGER, -- TODO: PRECISION
    NombreTipo TEXT,
    FOREIGN KEY (NombreTipo) REFERENCES Tipo(Nombre)
);

-- 6. Tabla: Pokémon (Instancia individual)
CREATE TABLE IF NOT EXISTS Pokemon (
    idPokemon INTEGER PRIMARY KEY AUTOINCREMENT,
    NombreCustom TEXT,
    Rareza INT, -- TODO: RAREZA
    Shiny BOOLEAN, -- TODO: SHINY
    Altura REAL,
    Peso REAL,
    NombreEspecie TEXT,
    FOREIGN KEY (NombreEspecie) REFERENCES EspeciePokemon(Nombre)
);

-- 7. Tabla: Equipo
CREATE TABLE IF NOT EXISTS Equipo (
    idEquipo INTEGER PRIMARY KEY AUTOINCREMENT, -- TODO: IdEquipo
    NombreUsuario TEXT,
    FOREIGN KEY (NombreUsuario) REFERENCES Usuario(NombreUsuario)
);

-- 8. Tabla: Opción Chatbot
CREATE TABLE IF NOT EXISTS OpcionChatbot (
    Opcion TEXT PRIMARY KEY,
    Descripcion TEXT
);

--- TABLAS DE RELACIÓN (Muchos a Muchos) ---

-- 9. Amigo de (Relación recursiva de Usuario)
CREATE TABLE IF NOT EXISTS AmigoDe (
    NombreUsuario1 TEXT,
    NombreUsuario2 TEXT,
    PRIMARY KEY (NombreUsuario1, NombreUsuario2),
    FOREIGN KEY (NombreUsuario1) REFERENCES Usuario(NombreUsuario),
    FOREIGN KEY (NombreUsuario2) REFERENCES Usuario(NombreUsuario)
);

-- 10. Publica (Relación Usuario - Contenido)
CREATE TABLE IF NOT EXISTS Publica (
    NombreUsuario TEXT,
    FechaHora DATETIME, -- TODO: FechaHora
    Contenido TEXT,
    PRIMARY KEY (NombreUsuario, FechaHora),
    FOREIGN KEY (NombreUsuario) REFERENCES Usuario(NombreUsuario)
);

-- 11. PokemonEnEquipo
CREATE TABLE IF NOT EXISTS PokemonEnEquipo (
    idEquipo INTEGER,
    idPokemon INTEGER,
    PRIMARY KEY (idEquipo, idPokemon),
    FOREIGN KEY (idEquipo) REFERENCES Equipo(idEquipo),
    FOREIGN KEY (idPokemon) REFERENCES Pokemon(idPokemon)
);

-- 12. AtaquePokemon (Ataques específicos que tiene un Pokémon individual)
CREATE TABLE IF NOT EXISTS AtaquePokemon (
    idPokemon INTEGER,
    nombreAtaque TEXT,
    PRIMARY KEY (idPokemon, nombreAtaque),
    FOREIGN KEY (idPokemon) REFERENCES Pokemon(idPokemon),
    FOREIGN KEY (nombreAtaque) REFERENCES Ataques(Nombre)
);

-- 13. PuedeUtilizar (Ataques que una especie puede aprender)
CREATE TABLE IF NOT EXISTS PuedeUtilizar (
    NombreEspecie TEXT,
    NombreAtaque TEXT,
    PRIMARY KEY (NombreEspecie, NombreAtaque),
    FOREIGN KEY (NombreEspecie) REFERENCES EspeciePokemon(Nombre),
    FOREIGN KEY (NombreAtaque) REFERENCES Ataques(Nombre)
);

-- 14. EspecieTipo (Relación entre especie y sus tipos)
CREATE TABLE IF NOT EXISTS EspecieTipo (
    NombreEspecie TEXT,
    NombreTipo TEXT,
    PRIMARY KEY (NombreEspecie, NombreTipo),
    FOREIGN KEY (NombreEspecie) REFERENCES EspeciePokemon(Nombre),
    FOREIGN KEY (NombreTipo) REFERENCES Tipo(Nombre)
);

-- 15. EfectoTipo (Tabla de efectividades/debilidades)
CREATE TABLE IF NOT EXISTS EfectoTipo (
    NombreTipo1 TEXT,
    NombreTipo2 TEXT,
    Efecto TEXT,
    PRIMARY KEY (NombreTipo1, NombreTipo2),
    FOREIGN KEY (NombreTipo1) REFERENCES Tipo(Nombre),
    FOREIGN KEY (NombreTipo2) REFERENCES Tipo(Nombre)
);


-- Insertar entidades para pruebas
-- Tata
INSERT OR IGNORE INTO Usuario VALUES ("Tata430", "Tata", "Morente", "tata@hotmail.es", "5678tata", "activa", FALSE);

--Tate
INSERT OR IGNORE INTO Usuario Values ( "Tate430", "Aco", "ElZapas", "marlartate@gmail.com", "1234tate", "activisimo", FALSE );

INSERT OR IGNORE INTO EspeciePokemon VALUES ("Pikachu", "Caca", FALSE, 1.75, 1.43, "Canto");

-- Tata
INSERT OR IGNORE INTO Pokemon VALUES (NULL,"Jon", 1, FALSE, 1.5, 1.5, "Pikachu");
INSERT OR IGNORE INTO Pokemon VALUES (NULL,"Laura", 8, FALSE, 1.1, 1.1, "Pikachu");

-- Tate
INSERT OR IGNORE INTO Pokemon VALUES (NULL, "Victor", 10, FALSE, 1.9, 1.5, "Pikachu");

-- Tata
INSERT OR IGNORE INTO Equipo VALUES (NULL, "Tata430");
-- Tate
INSERT OR IGNORE INTO Equipo VALUES (NULL, "Tate430");

-- Tata
INSERT OR IGNORE INTO PokemonEnEquipo VALUES (1, 1);
INSERT OR IGNORE INTO PokemonEnEquipo VALUES (1, 2);

-- Tate
INSERT OR IGNORE INTO PokemonEnEquipo VALUES (2, 3);