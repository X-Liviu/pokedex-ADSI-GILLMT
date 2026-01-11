from app.database.connection import Connection
from app.model.utils.custom_types import Custom_types
import json

class ChatBot: pass

class ChatBot :

    myChatBot: ChatBot = None
    def __init__(self, db: Connection):
        if ChatBot.myChatBot == None:
            self.db: Connection = db
            ChatBot.myChatBot = self
        else:
            raise Custom_types.SingletonError()

    @classmethod
    def getChatBot(cls, db: Connection) -> ChatBot:
        if cls.myChatBot == None:
            ChatBot(db)
        return cls.myChatBot

    def mostrarOpciones(self) :
        filas = self.db.select(
            sentence="SELECT * FROM OpcionChatbot"
        )
        json_opciones = []
        for fila in filas:
            json_opciones.append({
                "Opción": fila["Opcion"],
                "Descripción": fila["Descripcion"],
            })
        return json.dumps(json_opciones, indent=4)