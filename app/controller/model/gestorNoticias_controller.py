from ...database.connection import Connection

class gestorNoticias: pass

class gestorNoticias:
    myGestorNoticias: gestorNoticias = None


    def __init__(self):
        self.db = Connection()

    @classmethod
    def getGestorNoticias(cls, db: Connection):
        return cls.myGestorNoticias


    def mostrar_changelog(self, usuario):
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
            ORDER BY P.FechaHora DESC;
        """

        filas = self.db.select(sql, (usuario, usuario))
        json_noticia = []

        for fila in filas:
            json_noticia.append({
                "NombreUsuario": fila["NombreUsuario"],
                "FechaHora": fila["FechaHora"],
                "contenido": fila["Contenido"]
            })

        return json_noticia