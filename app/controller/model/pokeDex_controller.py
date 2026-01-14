import json
from app.model.especie import Especie

class PokeDex:
    _instance = None  # Aquí guardaremos la instancia única

    def __init__(self, listaEspecies: list):
        # Si ya existe una instancia, evitamos que se cree otra por error
        if PokeDex._instance is not None:
            raise Exception("Esta clase es un Singleton. Usa get_instance()")

        self.listaEspecies = listaEspecies
        PokeDex._instance = self

    @classmethod
    def get_instance(cls, listaEspecies=None):
        """
        Si no existe la Pokedex, la crea. Si ya existe, la devuelve.
        """
        if cls._instance is None:
            if listaEspecies is None:
                listaEspecies = []
            PokeDex(listaEspecies)
        return cls._instance

    # ---------------------------------------------------------
    # MÉTODOS DE BÚSQUEDA Y FILTRADO (Originales de PokeDex)
    # ---------------------------------------------------------

    def buscarEspecie(self, nombreEspecie):
        """
        Busca un objeto Especie dentro de la lista de la Pokedex.
        Devuelve el objeto Especie o None.
        """
        for especie in self.listaEspecies:
            if especie.esEsta(nombreEspecie):
                return especie
        return None

    def mostrarPokedex(self) -> str:
        lista_final = []
        for especie in self.listaEspecies:
            lista_final.append(especie.getInfo())

        return json.dumps(lista_final, indent=4)

    def getInfo(self, nombreEspecie: str) -> str:
        """
        Busca un Pokémon específico y devuelve su JSON formateado.
        """
        for especie in self.listaEspecies:
            if especie.nombre.lower() == nombreEspecie.lower():
                return json.dumps(especie.getInfo(), indent=4, ensure_ascii=False)
        return json.dumps({"error": "Pokémon no encontrado"})

    def filtrarPokedex(self, filtro: str, valor: str) -> str:
        lista_filtrada = []
        # Bucle para cada especie pokemon
        for especie in self.listaEspecies:
            if especie.comprobarFiltroValor(filtro, valor):
                lista_filtrada.append(especie.getInfo())

        return json.dumps(lista_filtrada, indent=4, ensure_ascii=False)

    # ---------------------------------------------------------
    # MÉTODOS INTEGRADOS (Provenientes de gestorPokeDex)
    # ---------------------------------------------------------

    def obtenerEfectos(self, nombreEspecie):
        """
        Devuelve un JSON con las debilidades y fortalezas de la especie.
        """
        laEspecie = self.buscarEspecie(nombreEspecie)
        if laEspecie is not None:
            datos = {
                "Efectos contra los que es fuerte": laEspecie.esFuerteContra(),
                "Efectos contra los que es débil": laEspecie.esDebilContra()
            }
            return datos
        else:
            return -1

    def caracteristicasPokemon(self, nombreEspecie):
        """
        Devuelve el diccionario de información (sin dumps) o -1 si no existe.
        Nota: Similar a getInfo, pero mantiene el retorno original del gestor.
        """
        laEspecie = self.buscarEspecie(nombreEspecie)
        if laEspecie is not None:
            return laEspecie.getInfo()
        else:
            return -1

    def cadenaEvolutiva(self, nombreEspecie):
        """
        Devuelve la cadena evolutiva de la especie.
        """
        laEspecie = self.buscarEspecie(nombreEspecie)
        if laEspecie is not None:
            return laEspecie.cadenaEvolutiva()
        else:
            return -1

    def añadirPokemon(self, nomPokemon, descr, legendario, altMedia, pesoMedio, region):
        """
        Paso 24aa: Crea la instancia de Especie y la añade a la lista.
        """
        # Paso 25aa: especies.add(new EspeciePokemon(...))
        # Añadimos los argumentos que faltan con valores por defecto para evitar el TypeError
        nueva_especie = Especie(
            nombre=nomPokemon,
            descripcion=descr,
            legendario=legendario,
            alturaMedia=altMedia,
            pesoMedio=pesoMedio,
            movimientos=[],      # Argumento requerido por Especie.__init__
            tipos=[],            # Argumento requerido por Especie.__init__
            imagen="",           # Argumento requerido por Especie.__init__
            evoluciones=[],      # Argumento requerido por Especie.__init__
            preevoluciones=[]    # Argumento requerido por Especie.__init__
        )
        self.listaEspecies.append(nueva_especie)

    def reiniciarPokedex(self):
        """
        Vacía la lista de especies para evitar duplicados al recargar datos.
        """
        self.listaEspecies = []
        print("[DEBUG] Pokedex reiniciada (Memoria limpia).")