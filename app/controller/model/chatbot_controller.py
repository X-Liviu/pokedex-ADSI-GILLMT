from app.database.connection import Connection
from app.model.utils.custom_types import Custom_types
import json

class ChatBot: pass

class ChatBot :

    myChatBot: ChatBot = None
    def __init__(self):
        self.db = Connection()


    @classmethod
    def getChatBot(cls, db=None):
        if cls.myChatBot is None:
            cls.myChatBot = ChatBot()
        return cls.myChatBot

    def mostrarOpciones(self) :
        filas = self.db.select(
            sentence="SELECT * FROM OpcionChatbot"
        )
        opciones = []
        for fila in filas:
            opciones.append({
                "Opción": fila["Opcion"],
                "Descripción": fila["Descripcion"],
            })
        return opciones