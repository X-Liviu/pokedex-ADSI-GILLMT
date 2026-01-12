from ...database.connection import Connection

class gestorNoticias: pass

class gestorNoticias:
    myGestorNoticias: gestorNoticias = None


    def __init__(self):
        self.db = Connection()

    @classmethod
    def getGestorNoticias(cls, db=None):
        if cls.myGestorNoticias is None:
            cls.myGestorNoticias = gestorNoticias()
        return cls.myGestorNoticias


    def mostrar_changelog(self, usuario, filtro):
        sql = """
            SELECT 
                P.NombreUsuario, 
                P.FechaHora, 
                P.Contenido
            FROM Publica P
            WHERE P.FechaHora >= DATE('now', '-1 month')
            AND P.NombreUsuario IN (
                SELECT A.NombreUsuario2 
                FROM AmigoDe A 
                WHERE A.NombreUsuario1 = ?
                
                UNION
                
                SELECT A.NombreUsuario1 
                FROM AmigoDe A 
                WHERE A.NombreUsuario2 = ?
            )
            AND NombreUsuario LIKE ? || '%'

            ORDER BY P.FechaHora DESC;
        """

        filas = self.db.select(sql, (usuario, usuario, filtro))
        json_noticia = []

        for fila in filas:
            json_noticia.append({
                "NombreUsuario": fila["NombreUsuario"],
                "FechaHora": fila["FechaHora"],
                "Contenido": fila["Contenido"]
            })

        return json_noticia