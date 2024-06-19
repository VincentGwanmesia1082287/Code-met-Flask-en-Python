import sqlite3
from flask import flash, session
from datetime import datetime
from lib.models.db_conn import DBConn

database = DBConn()

class Statements():

    def __init__(self, studentennummer, statement_number, value):
        self.studentennummer = studentennummer
        self.naam = statement_number
        self.klas = value

    
    def instert_statements(studentennummer, statement_number, value):
        #print("in class")
        connection = database.connect_database()
        #print("made connection to db")
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        crsr.execute("SELECT action_type FROM studenten WHERE studentnummer = ?", (studentennummer,))
        #print("in db")
        myresult = crsr.fetchone()
        if myresult[0] == None:
            crsr.execute("UPDATE studenten SET action_type = ?, last_completed_statement = ? WHERE studentnummer = ?", (value, statement_number, studentennummer,))
            connection.commit()
            connection.close()
            print("✅ value has been added successfully")
            return(statement_number)
            #return False
        else:
            newvalue = myresult[0] + value
            crsr.execute("UPDATE studenten SET action_type = ?, last_completed_statement = ? WHERE studentnummer = ?", (newvalue, statement_number, studentennummer,))
            connection.commit()
            connection.close()
            return(statement_number)
        # close the connection
