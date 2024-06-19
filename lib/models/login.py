import sqlite3
import bcrypt
from flask import flash, session
from datetime import datetime
from lib.models.db_conn import DBConn

database = DBConn()

class Login():

    def __init__(self, ID, Naam, Email, Wachtwoord, Actief_sinds):
        self.ID = ID
        self.Naam = Naam
        self.Email = Email  
        self.Wachtwoord = Wachtwoord    
        self.Actief_sinds = Actief_sinds
    
    def login(email, wachtwoord):
        connection = database.connect_database()
        #print("made connection to db")
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        crsr.execute("SELECT Wachtwoord, Naam, Is_admin FROM teachers WHERE Email = ?", (email,))
        #print("in db")
        myresult = crsr.fetchone()
        if myresult is None:
            return False, "Email does not exist."
        else:
            wachtwoordnieuw = myresult[0].encode('utf-8')
            result = bcrypt.checkpw(wachtwoord.encode('utf-8'), wachtwoordnieuw)
            if result:
                if myresult[2] == 1:
                    return True, "Welcome " + myresult[1], True
                else:
                    return True, "Welcome " + myresult[1], False
                
            else:
                return False, "Incorrect password."
        # close the connection
