import mysql.connector

class DbManager:

    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database
            )
            return connection
        except mysql.connector.Error as e:
            print("Errore di connessione al database:", str(e))
            