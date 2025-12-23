class ChatBot :
    def __init__(self, db) :
        self.db = db

    def mostrarOpciones(self) :
        rows = self.db.select(
            sentence="SELECT * FROM opciones"
        )
        return [dict(row) for row in rows]