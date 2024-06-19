import sqlite3
from flask import flash, session
from datetime import datetime
from lib.models.db_conn import DBConn
import bcrypt

database = DBConn()

class Teacher():

    def __init__(self, ID, Naam, Email, Wachtwoord):
        self.ID = ID
        self.Naam = Naam
        self.Email = Email
        self.Wachtwoord = Wachtwoord

    def read():
        connection = database.connect_database()
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        #teacher_id = session['authenticated_teacher']['teacher_id']
        crsr.execute("SELECT * FROM teachers WHERE del=0 ORDER BY ID;")
        myresult = crsr.fetchall()
        teacher_list = [dict(row) for row in myresult] # this is how it supposed to get the data from the database and pass it to the template
        teacher_list = [dict(row) for row in myresult]
        for teacher in teacher_list:
            date_time_obj = datetime.strptime(teacher['Actief_sinds'], '%Y-%m-%d %H:%M:%S')
            teacher['Actief_sinds'] = date_time_obj.strftime('%d-%m-%Y')
        connection.close()
        return teacher_list
    
    def add_teacher(email, naam, wachtwoord, is_admin):
        if is_admin:
            is_admin = 1
        else:
            is_admin = 0
        connection = database.connect_database()
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        crsr.execute("SELECT Email FROM teachers WHERE Email = ? AND del = 0", (email,))
        myresult = crsr.fetchall()
        teacher_list = [dict(row) for row in myresult]
        if len(teacher_list) == 0:
            hashed_password = bcrypt.hashpw(wachtwoord.encode('utf-8'), bcrypt.gensalt())
            crsr.execute("INSERT INTO teachers (Naam, Email, Wachtwoord, Is_admin) VALUES (?, ?, ?, ?)", (naam, email, hashed_password, is_admin))
            connection.commit()
            connection.close()
            print("✅ Teacher has been added successfully")
            return(True, "leraar is toegevoegd")
            #return False
        else:
            connection.close()
            return(False, "Leraar bestaat al")

    
    def get_for_edit(ID):
        print("in get for edit")
        connection = database.connect_database()
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        #teacher_id = session['authenticated_teacher']['teacher_id']
        crsr.execute("SELECT ID, Naam, Email, Is_admin FROM teachers WHERE ID = ?;", (ID,))
        myresult = crsr.fetchall()
        teacher_list = [dict(row) for row in myresult] # this is how it supposed to get the data from the database and pass it to the template
        connection.close()
        print(teacher_list)
        return teacher_list
    
    def update_teacher(ID, Naam, Email, is_admin):
        if is_admin:
            is_admin = 1
        else:
            is_admin = 0
        connection = database.connect_database()
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        #teacher_id = session['authenticated_teacher']['teacher_id']
        crsr.execute("UPDATE teachers SET Naam = ?, Email = ?, Is_admin = ? WHERE ID = ?", (Naam, Email, is_admin, ID))
        connection.commit()
        connection.close()
        return "gebruiker is geupdate"
    
    def delete_teacher(ID):
        connection = database.connect_database()
        connection.row_factory = sqlite3.Row
        crsr = connection.cursor()
        #teacher_id = session['authenticated_teacher']['teacher_id']
        crsr.execute("UPDATE teachers SET del = -1 WHERE ID = ?", (ID,))
        connection.commit()
        connection.close()
        return "gebruiker is verwijderd"