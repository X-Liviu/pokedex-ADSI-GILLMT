from ...database.connection import Connection

class gestorNoticias: pass

class gestorNoticias:
    myGestorNoticias: gestorNoticias = None


    def __init__(self, db):
        self.db = db

    @classmethod
    def getGestorNoticias(cls, db=None):
        if cls.myGestorNoticias is None:
            cls.myGestorNoticias = gestorNoticias(db)
        return cls.myGestorNoticias


    def mostrar_changelog(self, usuario, filtro, db):
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
            )
            AND NombreUsuario LIKE ? || '%'

            ORDER BY P.FechaHora DESC;
        """

        filas = db.select(sql, (usuario, filtro))
        json_noticia = []

        for fila in filas:
            json_noticia.append({
                "NombreUsuario": fila["NombreUsuario"],
                "FechaHora": fila["FechaHora"],
                "Contenido": fila["Contenido"]
            })

        return json_noticia

    def aniadirNoticia(self, nombreUsuario, descripcion, db):
        sql = """ 
            INSERT INTO Publica (nombreUsuario, FechaHora, Contenido)
			VALUES (?, DATETIME('now'), ? )
        """
        db.insert(sql,(nombreUsuario, descripcion))
