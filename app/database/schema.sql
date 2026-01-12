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

-- 16. Relacion evoluciones Pokémon
CREATE TABLE Evolucion (
    Evolucion TEXT,
    Preevolucion TEXT,
    PRIMARY KEY (Evolucion, Preevolucion),
    FOREIGN KEY (Evolucion) REFERENCES EspeciePokemon(Nombre),
    FOREIGN KEY (Preevolucion) REFERENCES EspeciePokemon(Nombre)
);


--- INSERTAR DATOS DE PRUEBA ---

-- A. Insertar Usuarios Originales
INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol) VALUES ('LiviuX', 'Liviu', 'Deleanu', 'ash@pueblopaleta.com', '1234', 'VERIF');
INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol) VALUES ('TataX', 'Tabata', 'Morente', 'tata@kanto.net', '1234', 'VERIF');
INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol) VALUES ('GorkaX', 'Gorka', 'Bidaguren', 'gorki@pokedex.org', '1234', 'ADMIN');
INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol) VALUES ('LauraX', 'Laura', 'Calvo', 'laura@celeste.com', '1234', 'VERIF');
INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol) VALUES ('MarcoX', 'Marco', 'Lartategui', 'marco@teamrocket.com', '1234', 'NOVERIF');
INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol) VALUES ('IkerX', 'Iker', 'Fuente', 'iker@oak.net', '1234', 'VERIF');
INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol) VALUES ('AshKetchum', 'Ash', 'Ketchum', 'real_ash@kanto.com', '1234', 'VERIF');
INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol) VALUES ('GaryOak', 'Gary', 'Oak', 'gary_champ@kanto.com', '1234', 'VERIF');
INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol) VALUES ('Misty', 'Misty', 'Waterflower', 'misty@cerulean.com', '1234', 'VERIF');
INSERT OR IGNORE INTO Usuario (NombreUsuario, Nombre, Apellido, Correo, Contrasena, Rol) VALUES ('Brock', 'Brock', 'Harrison', 'brock@pewter.com', '1234', 'VERIF');


-- B. Datos necesarios para que los equipos funcionen (Región, Especie)
INSERT OR IGNORE INTO Pokedex VALUES ('Kanto', 'Primera');
INSERT OR IGNORE INTO EspeciePokemon VALUES ('Pikachu', 'Ratón eléctrico', FALSE, 0.4, 6.0, 'Kanto');
INSERT OR IGNORE INTO EspeciePokemon VALUES ('Eevee', 'Evolución', FALSE, 0.3, 6.5, 'Kanto');

-- C. Pokémons individuales (Instancias)
-- Pikachu de Ash
INSERT OR IGNORE INTO Pokemon (idPokemon, numPokemon, NombreCustom, Rareza, Shiny, Altura, Peso, NombreEspecie, Imagen)
VALUES (1, 25, 'Pikachu', 5, FALSE, 0.4, 6.0, 'Pikachu', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png');

-- Eevee de Gary
INSERT OR IGNORE INTO Pokemon (idPokemon, numPokemon, NombreCustom, Rareza, Shiny, Altura, Peso, NombreEspecie, Imagen)
VALUES (2, 133, 'Eevee', 4, FALSE, 0.3, 6.5, 'Eevee', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/133.png');

-- D. Equipos (Vinculados a Ash y Gary, que ahora ya existen)
INSERT OR IGNORE INTO Equipo (idEquipo, numEquipo, NombreUsuario) VALUES (1, 1, 'AshKetchum');
INSERT OR IGNORE INTO Equipo (idEquipo, numEquipo, NombreUsuario) VALUES (2, 1, 'GaryOak');

-- E. Relación Pokemon - Equipo
INSERT OR IGNORE INTO PokemonEnEquipo (idEquipoInterno, idPokemon) VALUES (1, 1); -- Pikachu en equipo de Ash
INSERT OR IGNORE INTO PokemonEnEquipo (idEquipoInterno, idPokemon) VALUES (2, 2); -- Eevee en equipo de Gary

-- F. Opción ChatBot
INSERT OR IGNORE INTO OpcionChatbot VALUES('1', 'Dado un equipo Pokémon, devolver cual es el mejor.');

-- G. AMIGOS (NUEVA SECCIÓN)
-- Amigos para 'LiviuX':
INSERT OR IGNORE INTO AmigoDe (NombreUsuario1, NombreUsuario2) VALUES ('LiviuX', 'TataX');
INSERT OR IGNORE INTO AmigoDe (NombreUsuario1, NombreUsuario2) VALUES ('LiviuX', 'GorkaX');
INSERT OR IGNORE INTO AmigoDe (NombreUsuario1, NombreUsuario2) VALUES ('LiviuX', 'AshKetchum');
INSERT OR IGNORE INTO AmigoDe (NombreUsuario1, NombreUsuario2) VALUES ('LiviuX', 'Misty');

-- Amigos para 'TataX':
INSERT OR IGNORE INTO AmigoDe (NombreUsuario1, NombreUsuario2) VALUES ('TataX', 'LiviuX');
INSERT OR IGNORE INTO AmigoDe (NombreUsuario1, NombreUsuario2) VALUES ('TataX', 'LauraX');

-- Amigos para 'AshKetchum':
INSERT OR IGNORE INTO AmigoDe (NombreUsuario1, NombreUsuario2) VALUES ('AshKetchum', 'GaryOak');
INSERT OR IGNORE INTO AmigoDe (NombreUsuario1, NombreUsuario2) VALUES ('AshKetchum', 'Misty');
INSERT OR IGNORE INTO AmigoDe (NombreUsuario1, NombreUsuario2) VALUES ('AshKetchum', 'Brock');

-- Amigos para 'GorkaX' (Admin):
INSERT OR IGNORE INTO AmigoDe (NombreUsuario1, NombreUsuario2) VALUES ('GorkaX', 'IkerX');

-- 7. NOTICIAS DE USUARIOS

-- se deberían mostrar --
INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('GorkaX', DATETIME('now', '-2 day'), '⚠️ Atención entrenadores: Se acerca una actualización en el sistema de Rankings. ¡Aseguraos de guardar vuestros equipos! 🛠️📊');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('AshKetchum', DATETIME('now', '-3 hour'), '¡Pikachu y yo acabamos de ganar una batalla imposible! ⚡🧢 Nunca hay que rendirse. ¡A por la siguiente medalla! 🏅');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('LiviuX', DATETIME('now', '-1 day'), '¡NO ME LO CREO! 😱 Acabo de encontrarme un Charizard Variocolor (Shiny) salvaje. 🔥✨ ¡La suerte está de mi lado hoy!');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('Misty', DATETIME('now', '-2 day'), 'Busco entrenador experto en tipo Agua para intercambio. Ofrezco Starmie con IVs perfectos. 💧⭐ Solo ofertas serias, por favor.');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('GaryOak', DATETIME('now', '-3 day'), 'Mientras vosotros seguís atrapando Rattatas, yo ya estoy entrenando para la Liga. 👋😎 Nos vemos en la cima (o no). #MarcodexChampion');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('TataX', DATETIME('now', '-7 day'), 'Estoy montando un equipo monotype de Hada 🧚‍♀️. ¿Alguien me recomienda un buen tanque defensivo? Estaba pensando en Clefable. 💕');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('Brock', DATETIME('now', '-14 day'), 'La clave para un Onix fuerte no es solo el entrenamiento, es una buena dieta de rocas ricas en minerales. 🪨🍲 ¡Mis recetas nunca fallan!');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('IkerX', DATETIME('now', '-1 month'), '¡Torneo amistoso este fin de semana en Ciudad Verde! 🌲⚔️ Inscripciones abiertas por mensaje privado. ¡Demostrad vuestro poder!');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('LauraX', DATETIME('now', '-2 month'), '¿Alguien sabe dónde puedo conseguir una Piedra Noche? 🌑 Mi Murkrow la necesita urgentemente. ¡Ayuda! 🦅');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('GorkaX', DATETIME('now', '-30 minute'), '🔧 Mantenimiento: Estamos ajustando los servidores del PC de Bill. Si notáis lag al transferir Pokémon, es normal. 💻🔌');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('MarcoX', DATETIME('now', '-5 hour'), '¡Increíble! El Team Rocket me ha intentado robar el bocadillo en vez de al Pikachu. 🍙😠 Están desesperados... 🚀');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('LauraX', DATETIME('now', '-12 hour'), 'Hay una Incursión de Tyranitar 5⭐ cerca del gimnasio. ¿Quién se apunta? Necesito gente con tipo Lucha. 🦖👊');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('IkerX', DATETIME('now', '-1 day', '-2 hour'), 'Tras 300 huevos... ¡Por fin salió! Scizor Firme con Técnica Experto. 🥚🦀✨ La paciencia da sus frutos.');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('AshKetchum', DATETIME('now', '-3 day', '-5 hour'), '¿Alguien sabe dónde hacen las mejores hamburguesas en Ciudad Trigal? 🍔 Snorlax y yo nos morimos de hambre. 🤤');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('TataX', DATETIME('now', '-5 day'), '¡Milotic ha ganado la cinta de Belleza en el Concurso Pokémon! 🎀💅 Mirad qué brillo tiene sus escamas. ¡Guapísimo! 💖');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('Brock', DATETIME('now', '-7 day', '-1 hour'), 'La Agente Mara de Ciudad Plateada tiene algo especial... 😍 Lástima que su Growlithe casi me muerde la pierna. 👮‍♀️🐕 #AmorImposible');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('GaryOak', DATETIME('now', '-14 day'), 'He visto vuestros equipos en el Ranking... patéticos. 📉😂 A ver si entrenáis más y lloráis menos. ¡Nos vemos en la Liga! 👋');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('LiviuX', DATETIME('now', '-21 day'), 'Necesito a alguien de confianza para evolucionar a mi Haunter. 👻🤝 Lo paso, evoluciona a Gengar y me lo devolvéis. ¿Voluntarios?');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('Misty', DATETIME('now', '-1 month', '-2 day'), 'Psyduck ha vuelto a salir de la Pokéball solo y le duele la cabeza... otra vez. 🦆🤕 ¡Qué paciencia hay que tener! 💧');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('GorkaX', DATETIME('now', '-2 month'), '🐛 Bug detectado: Algunos usuarios reportan que MissingNo está apareciendo en la costa de Isla Canela. ¡NO LO ATRAPÉIS! Corrompe la partida. 🚫👾');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('LauraX', DATETIME('now', '-2 month', '-15 day'), '¡Solo me falta Celebi para completar la Pokédex de Johto! 🌿🧚‍♀️ ¿Es verdad que aparece en el Encinar si usas la GS Ball? 🤔');


-- NO se deberían mostrar --
INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('MarcoX', DATETIME('now', '-4 month'), 'Probando la nueva Marcodex. ¿Esto funciona? 🎤🐢 (Este mensaje es antiguo y no debería salir).');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('AshKetchum', DATETIME('now', '-6 month'), 'Hoy salgo de Pueblo Paleta. ¡Voy a ser el mejor que habrá jamás! 🎒🌍');

INSERT INTO Publica (NombreUsuario, FechaHora, Contenido)
VALUES ('GaryOak', DATETIME('now', '-1 year'), 'Eligiendo a Squirtle. Claramente la mejor opción. 🐢💧 ¡Adiós perdedores!');