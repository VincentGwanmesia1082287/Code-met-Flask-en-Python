import sqlite3
from flask import flash, session
from datetime import datetime
from lib.models.db_conn import DBConn

database = DBConn()

class Studentennummer():

    def __init__(self, studentennummer, naam, klas, ingevuld, action_type, team):
        self.studentennummer = studentennummer
        self.naam = naam
        self.klas = klas
        self.ingevuld = ingevuld
        self.action_type = action_type
        self.team = team

    
    def check_student(studentennummer):
        print("in class")
        connection = database.connect_database()
        print("made connection to db")
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        crsr.execute("SELECT studentnummer, Naam, Klas, last_completed_statement FROM studenten WHERE studentnummer = ?", (studentennummer,))
        print("in db")
        myresult = crsr.fetchall()
        student_list = [dict(row) for row in myresult]
        if len(student_list) == 0:
            return(False)
            #return False
        else:
            # close the connection
            connection.close()
            if student_list[0]['last_completed_statement'] == None:
                return(True, "0", student_list[0]['studentnummer'], student_list[0]['Naam'], student_list[0]['Klas'])
            else:
                return(True, student_list[0]['last_completed_statement'], student_list[0]['studentnummer'], student_list[0]['Naam'], student_list[0]['Klas'])

    def read():
        connection = database.connect_database()
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        #teacher_id = session['authenticated_teacher']['teacher_id']
        crsr.execute("SELECT * FROM studenten WHERE del=0 ORDER BY Klas DESC;")
        myresult = crsr.fetchall()
        student_list = [dict(row) for row in myresult] # this is how it supposed to get the data from the database and pass it to the template
        connection.close()
        return student_list
    
    def get_for_edit(studentennummer):
        connection = database.connect_database()
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        #teacher_id = session['authenticated_teacher']['teacher_id']
        crsr.execute("SELECT studentnummer, Naam, Klas FROM studenten WHERE studentnummer = ?;", (studentennummer,))
        myresult = crsr.fetchall()
        student_list = [dict(row) for row in myresult] # this is how it supposed to get the data from the database and pass it to the template
        connection.close()
        return student_list
    
    def update_student(studentennummer, naam, klas):
        connection = database.connect_database()
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        #teacher_id = session['authenticated_teacher']['teacher_id']
        crsr.execute("UPDATE studenten SET studentnummer = ?, Naam = ?, Klas = ? WHERE studentnummer = ?", (studentennummer, naam, klas, studentennummer,))
        connection.commit()
        connection.close()
        return "gebruiker is geupdate"
    
    def delete_student(studentennummer):
        connection = database.connect_database()
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        #teacher_id = session['authenticated_teacher']['teacher_id']
        crsr.execute("UPDATE studenten SET del = -1 WHERE studentnummer = ?", (studentennummer,))
        connection.commit()
        connection.close()
        return "gebruiker is verwijderd"
    
    def get_code(studentnummer):
        connection = database.connect_database()
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        crsr.execute("SELECT action_type FROM studenten WHERE studentnummer = ?", (studentnummer,))
        myresult = crsr.fetchone()
        connection.close()
        return myresult[0]
    
    def opnieuw(studentnummer):
        print("in class")
        connection = database.connect_database()
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        crsr.execute("UPDATE studenten SET action_type = '',  last_completed_statement = 0 WHERE studentnummer = ?", (studentnummer,))
        connection.commit()
        connection.close()
        return "vragenlijst is opnieuw gestart"