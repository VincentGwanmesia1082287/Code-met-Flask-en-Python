import sqlite3

class DBConn:
    
    def connect_database(self):
        connection = sqlite3.connect('database/database.db')
        connection.row_factory = sqlite3.Row
        return connection