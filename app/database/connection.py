import sqlite3

from config import Config


class Connection:

    def __init__(self):
        self.connection = sqlite3.connect(
            Config.DB_PATH,
            check_same_thread=False
        )
        self.connection.row_factory = sqlite3.Row
        self.__initialized = True


    def select(self, sentence, parameters=None):
        cursor = self.connection.cursor()
        if parameters:
            cursor.execute(sentence, parameters)
        else:
            cursor.execute(sentence)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def insert(self, sentence, parameters=None):
        cursor = self.connection.cursor()
        if parameters:
            cursor.execute(sentence, parameters)
        else:
            cursor.execute(sentence)
        self.connection.commit()

        # ESTO ES LO QUE FALTA: Capturamos el ID generado
        last_id = cursor.lastrowid

        cursor.close()
        return last_id  # Devolvemos el ID para usarlo en las otras tablas

    def update(self, sentence, parameters=None):
        cursor = self.connection.cursor()
        if parameters:
            cursor.execute(sentence, parameters)
        else:
            cursor.execute(sentence)
        self.connection.commit()
        cursor.close()


    def delete(self, sentence, parameters=None):
        cursor = self.connection.cursor()
        if parameters:
            cursor.execute(sentence, parameters)
        else:
            cursor.execute(sentence)
        self.connection.commit()
        cursor.close()
