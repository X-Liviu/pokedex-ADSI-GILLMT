import pytest
import re
from app.controller.model.gestorUsuario_controller import gestorUsuario
from conftest import Connection


# --- FUNCIONES AUXILIARES ---

def iniciar_sesion(p_cliente, pNombreUsuario: str):
    respuesta = p_cliente.post("/identificacion",
                               data={"usuario": pNombreUsuario, "contrasena": "1234"},
                               follow_redirects=True)
    assert respuesta.status_code == 200


def asegurar_equipo_test(client, usuario="TataX"):
    """Garantiza que existe un equipo con 'MoteBase' limpio y vinculado en BD."""
    db = Connection()
    iniciar_sesion(client, usuario)

    # 1. LIMPIEZA: Borramos restos de tests fallidos para que el equipo 1 esté "virgen"
    # Borramos relaciones y pokemon antiguos asociados al usuario para evitar el caos de IDs
    db.delete(
        "DELETE FROM PokemonEnEquipo WHERE idEquipoInterno IN (SELECT idEquipo FROM Equipo WHERE NombreUsuario = ?)",
        (usuario,))
    db.delete("DELETE FROM Equipo WHERE NombreUsuario = ?", (usuario,))

    # 2. CREACIÓN REAL: Pasamos por el flujo completo
    client.get('/crear-equipo')
    client.post('/crear-equipo', data={
        'accion': 'aniadir',
        'especie': 'Pikachu',
        'nombre_custom': 'MoteBase'
    })
    # Guardamos. Esto debería insertar en Equipo, Pokemon y PokemonEnEquipo
    client.post('/crear-equipo', data={'accion': 'guardar'}, follow_redirects=True)

    # 3. VERIFICACIÓN DOBLE: ¿Está el equipo Y está el bicho vinculado?
    res_eq = db.select("SELECT idEquipo FROM Equipo WHERE NombreUsuario = ? AND numEquipo = 1", (usuario,))

    if not res_eq:
        pytest.fail(f"Error: No se creó la entrada en la tabla Equipo para {usuario}")

    id_interno = res_eq[0][0]

    # Comprobamos la relación (Este era el punto ciego)
    res_vinc = db.select("SELECT * FROM PokemonEnEquipo WHERE idEquipoInterno = ?", (id_interno,))

    if not res_vinc:
        # Si el equipo existe pero no tiene bichos, el test de 'cambios mixtos' fallará al intentar borrar
        pytest.fail(f"Error: El equipo existe (ID {id_interno}) pero no tiene Pokémon vinculados en la BD")

    # Forzamos recarga en RAM
    client.get('/mis-equipos')
    return 1  # Devolvemos el numEquipo (que es 1)


# --- BLOQUE 1: CREAR EQUIPO ---

def test_aniadir_pokemon_exitoso(client):
    iniciar_sesion(client, "TataX")
    client.get('/crear-equipo')
    res = client.post('/crear-equipo', data={
        'accion': 'aniadir', 'especie': 'Pikachu', 'nombre_custom': 'PikaTata'
    }, follow_redirects=True)
    assert b"PikaTata" in res.data


def test_error_aniadir_misma_especie(client):
    iniciar_sesion(client, "TataX")
    client.get('/crear-equipo')
    client.post('/crear-equipo', data={'accion': 'aniadir', 'especie': 'eevee', 'nombre_custom': 'E1'})
    res = client.post('/crear-equipo', data={'accion': 'aniadir', 'especie': 'eevee', 'nombre_custom': 'E2'},
                      follow_redirects=True)
    assert b"especie" in res.data.lower() or b"equipo" in res.data.lower()


def test_borrar_pokemon_de_la_lista(client):
    iniciar_sesion(client, "TataX")
    client.get('/crear-equipo')
    mote = "BubaTest"
    res_aniadir = client.post('/crear-equipo', data={
        'accion': 'aniadir', 'especie': 'Bulbasaur', 'nombre_custom': mote
    }, follow_redirects=True)

    html = res_aniadir.data.decode('utf-8')
    match = re.search(r'name="pokemon_id" value="(\d+)"', html)

    if match:
        pokemon_id = match.group(1)
        res_final = client.post('/crear-equipo', data={'accion': 'borrar', 'pokemon_id': pokemon_id},
                                follow_redirects=True)
        assert mote.encode() not in res_final.data
        assert b"0/6" in res_final.data
    else:
        pytest.fail("No se encontró el ID en el equipo.")


def test_error_equipo_completo_con_seis_distintos(client):
    iniciar_sesion(client, "TataX")
    client.get('/crear-equipo')
    especies = ["Pikachu", "Eevee", "Bulbasaur", "Ivysaur", "Venusaur", "Charmander"]
    for i, esp in enumerate(especies):
        client.post('/crear-equipo', data={'accion': 'aniadir', 'especie': esp, 'nombre_custom': f'Mote{i}'})

    res = client.post('/crear-equipo', data={'accion': 'aniadir', 'especie': 'Charmeleon', 'nombre_custom': 'Extra'},
                      follow_redirects=True)
    assert b"completo" in res.data.lower() or b"6/6" in res.data


# --- BLOQUE 2: CANCELAR ---

def test_cancelar_creacion_vuelve_al_menu(client):
    iniciar_sesion(client, "TataX")
    res = client.post('/crear-equipo?origen=menu', data={'accion': 'cancelar'}, follow_redirects=True)
    assert b"Principal" in res.data or b"Ranking" in res.data


def test_aniadir_pokemon_y_cancelar_no_guarda_nada(client):
    iniciar_sesion(client, "TataX")
    client.get('/crear-equipo')
    client.post('/crear-equipo', data={'accion': 'aniadir', 'especie': 'pikachu', 'nombre_custom': 'PikaTemporal'})

    gestor = gestorUsuario.getMyGestorUsuario("TataX")
    num_antes = len(gestor.usuario.lista_equipos)

    client.post('/crear-equipo?origen=menu', data={'accion': 'cancelar'}, follow_redirects=True)
    assert len(gestor.usuario.lista_equipos) == (num_antes - 1)


# --- BLOQUE 3: GUARDAR ---

def test_guardar_equipo_completo_bd(client):
    iniciar_sesion(client, "TataX")
    mote_fijo = "MoteFijoGuardar"

    with client:
        client.get('/crear-equipo')
        client.post('/crear-equipo', data={
            'accion': 'aniadir', 'especie': 'Squirtle', 'nombre_custom': mote_fijo
        }, follow_redirects=True)
        client.post('/crear-equipo', data={'accion': 'guardar'}, follow_redirects=True)

    db = Connection()
    poki = db.select("SELECT * FROM Pokemon WHERE NombreCustom = ?", (mote_fijo,))
    assert len(poki) > 0


# --- BLOQUE 4: VER EQUIPOS ---

def test_ver_equipos_vacio_muestra_error_o_mensaje(client):
    iniciar_sesion(client, "Misty")
    res = client.get('/mis-equipos', follow_redirects=True)
    assert b"no tienes" in res.data.lower() or b"equipos" in res.data.lower()


def test_navegacion_mis_equipos(client):
    iniciar_sesion(client, "TataX")
    res = client.get('/mis-equipos')
    assert b"crear" in res.data.lower()


def test_acceso_a_detalles_y_enlace_modificar(client):
    iniciar_sesion(client, "TataX")
    n_eq = asegurar_equipo_test(client, "TataX")

    res_vista = client.get(f'/detalles-equipo/{n_eq}', follow_redirects=True)
    assert res_vista.status_code == 200
    html = res_vista.data.decode('utf-8')
    assert f"modificar-equipo/{n_eq}" in html or f"num_equipo={n_eq}" in html


# --- BLOQUE 5: MODIFICAR ---

def test_cancelar_edicion_sin_cambios(client):
    iniciar_sesion(client, "TataX")
    n_eq = asegurar_equipo_test(client, "TataX")

    res = client.post(f'/modificar-equipo/{n_eq}', data={'accion': 'cancelar'}, follow_redirects=True)
    assert res.status_code == 200
    assert b"equipos" in res.data.lower()


def test_aniadir_pokemon_en_edicion(client):
    n_eq = asegurar_equipo_test(client, "TataX")

    # 1. Creamos la copia en RAM
    client.get(f'/modificar-equipo/{n_eq}')

    # 2. Añadimos bicho a la RAM
    res = client.post(f'/modificar-equipo/{n_eq}', data={
        'accion': 'aniadir', 'especie': 'Eevee', 'nombre_custom': 'EditadoEevee'
    }, follow_redirects=True)

    assert b"EditadoEevee" in res.data


def test_cancelar_edicion_con_cambios_no_persiste(client):
    iniciar_sesion(client, "TataX")
    n_eq = asegurar_equipo_test(client, "TataX")

    mote_provisional = "NoGuardar"
    # Entramos (esto debería clonar)
    client.get(f'/modificar-equipo/{n_eq}')
    # Añadimos
    client.post(f'/modificar-equipo/{n_eq}',
                data={'accion': 'aniadir', 'especie': 'Eevee', 'nombre_custom': mote_provisional})
    # CANCELAMOS (esto debería descartar la copia)
    client.post(f'/modificar-equipo/{n_eq}', data={'accion': 'cancelar'}, follow_redirects=True)

    # Recargamos de la BD para ver el estado real "oficial"
    client.get('/mis-equipos')
    gestor = gestorUsuario.getMyGestorUsuario("TataX")
    equipo_real = next((e for e in gestor.usuario.lista_equipos if e.numEquipo == n_eq), None)

    assert all(p.nombre_custom != mote_provisional for p in
               equipo_real.lista_pokemon), "El cambio se quedó en el objeto real tras cancelar"


def test_borrar_pokemon_en_edicion(client):
    iniciar_sesion(client, "TataX")
    n_eq = asegurar_equipo_test(client, "TataX")

    # 1. Entramos para que se cree la copia
    client.get(f'/modificar-equipo/{n_eq}')

    # 2. Añadimos el bicho que queremos borrar
    client.post(f'/modificar-equipo/{n_eq}',
                data={'accion': 'aniadir', 'especie': 'Bulbasaur', 'nombre_custom': 'BorrarYa'},
                follow_redirects=True)

    # 3. Buscamos el ID específico de 'BorrarYa' en el HTML
    res_pag = client.get(f'/modificar-equipo/{n_eq}')
    html_content = res_pag.data.decode('utf-8')

    # Buscamos el bloque que contiene 'BorrarYa' y capturamos su value="ID"
    # Esta expresión regular es más precisa: busca el input oculto que está cerca del texto
    match = re.search(r'BorrarYa.*?value="(\d+)"', html_content, re.DOTALL)

    if not match:
        pytest.fail("No se encontró el mote 'BorrarYa' o su ID en el HTML")

    poki_id = match.group(1)

    # 4. Ejecutamos el borrado
    res_del = client.post(f'/modificar-equipo/{n_eq}',
                          data={'accion': 'borrar', 'pokemon_id': poki_id},
                          follow_redirects=True)

    # 5. VERIFICACIÓN: El mote ya no debe estar en el HTML
    assert b"BorrarYa" not in res_del.data, f"El bicho con ID {poki_id} no se borró de la RAM"


def test_guardar_edicion_sin_cambios(client):
    """Verifica que se puede guardar un equipo sin haber hecho modificaciones."""
    iniciar_sesion(client, "TataX")
    n_eq = asegurar_equipo_test(client, "TataX")

    # Entramos a editar
    client.get(f'/modificar-equipo/{n_eq}')

    # Guardamos directamente sin enviar acciones de añadir o borrar
    res = client.post(f'/modificar-equipo/{n_eq}', data={'accion': 'guardar'}, follow_redirects=True)

    # Debería redirigir a mis-equipos y mostrar el éxito
    assert res.status_code == 200
    assert b"Mis Equipos" in res.data or b"equipos" in res.data.lower()


def test_guardar_edicion_con_cambios_mixtos_persiste(client):
    """Verifica borrar y añadir, asegurando que el bicho base existe en disco."""
    iniciar_sesion(client, "TataX")
    n_eq = asegurar_equipo_test(client, "TataX")

    # Forzamos un guardado. Si el bicho ya está en RAM por el 'asegurar',
    # esto lo manda a la BD. Así el 'borrar' siguiente sí tendrá algo que borrar en el disco.
    client.post(f'/modificar-equipo/{n_eq}', data={'accion': 'guardar'}, follow_redirects=True)
    # ------------------------------------------------------

    mote_nuevo = "BichoNuevo"

    # 1. Entramos a la página y capturamos el ID de RAM
    res_get = client.get(f'/modificar-equipo/{n_eq}')
    html = res_get.data.decode('utf-8')
    match = re.search(r'MoteBase.*?name="pokemon_id" value="(\d+)"', html, re.DOTALL)
    id_ram_viejo = match.group(1)

    # 2. Identificamos el ID Real en BD (ahora sí existirá porque acabamos de guardar)
    db = Connection()
    res_p = db.select("SELECT idPokemon FROM Pokemon WHERE numPokemon = ? AND NombreCustom = 'MoteBase'",
                      (id_ram_viejo,))
    id_bd_viejo = res_p[0][0]

    # 3. ACCIONES EN RAM
    client.post(f'/modificar-equipo/{n_eq}', data={'accion': 'borrar', 'pokemon_id': id_ram_viejo})
    client.post(f'/modificar-equipo/{n_eq}',
                data={'accion': 'aniadir', 'especie': 'Squirtle', 'nombre_custom': mote_nuevo})

    # 4. GUARDADO FINAL
    client.post(f'/modificar-equipo/{n_eq}', data={'accion': 'guardar'}, follow_redirects=True)

    # 5. VERIFICACIÓN
    res_eq = db.select("SELECT idEquipo FROM Equipo WHERE numEquipo = ? AND NombreUsuario = ?", (n_eq, "TataX"))
    id_eq = res_eq[0][0]

    # El nuevo debe tener 1 vínculo, el viejo 0
    v_nuevo = db.select(
        "SELECT * FROM PokemonEnEquipo WHERE idEquipoInterno = ? AND idPokemon IN (SELECT idPokemon FROM Pokemon WHERE NombreCustom = ?)",
        (id_eq, mote_nuevo))
    v_viejo = db.select("SELECT * FROM PokemonEnEquipo WHERE idEquipoInterno = ? AND idPokemon = ?",
                        (id_eq, id_bd_viejo))

    assert len(v_nuevo) == 1, "El nuevo no se guardó"
    assert len(v_viejo) == 0, "El viejo no se borró"