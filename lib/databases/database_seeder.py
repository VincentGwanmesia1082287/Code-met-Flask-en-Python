import json
import sqlite3
from pathlib import Path
my_path = Path(__file__).parent.resolve()
project_root = my_path.parent.parent
students_path = project_root / "static/jsonfiles/students.json"

# Open het bestand student.json
with open(students_path, 'r') as file:
    # Lees de inhoud van het bestand
    data = json.load(file)
for student in data:
    connection = sqlite3.connect('database/database.db')
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO studenten (studentnummer, Naam, Klas, last_completed_statement) VALUES (?, ?, ?, 0)", (student["student_number"], student["student_name"], student["student_class"]))
    connection.commit()
    connection.close()
print("✅ user has been added successfully")	

statement_path = project_root / "static/jsonfiles/actiontype_statements.json"

# Open het bestand student.json
with open(statement_path, 'r') as file:
    # Lees de inhoud van het bestand
    datastatement = json.load(file)
for statement in datastatement:
    for choices in statement["statement_choices"]:
        connection = sqlite3.connect('database/database.db')
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO statement (choice_number, choice_text, choice_result) VALUES (?, ?, ?)", (choices["choice_number"], choices["choice_text"], choices["choice_result"]))
        connection.commit()
        connection.close()
print("✅ statement has been added successfully")
# Print de inhoud van het bestand

# List of sample names and emails
teachers = [
    {"naam": "Vincent", "email": "vincent@hr.nl", "Is_admin": "0"},
    {"naam": "Admin", "email": "admin@hr.nl", "Is_admin": "1"},
]
connection = sqlite3.connect('database/database.db')
cursor = connection.cursor()
# Seed data for each teacher
for teacher in teachers:
    naam = teacher["naam"]
    email = teacher["email"]
    is_admin = teacher["Is_admin"]
    wachtwoord = "$2a$12$cOc836sv4zdz7qItwLGeJOAi5EjlFHY.7n/QXaLTMCdr1JWFNCbsy"  # "password" hashed with bcrypt
    # Insert teacher data into the database
    cursor.execute(
            "INSERT INTO teachers (Naam, Email, Wachtwoord, Is_admin) VALUES (?, ?, ?, ?)", (naam, email, wachtwoord, is_admin))

# Commit changes and close connection
connection.commit()
connection.close()
print("✅ teacher has been added successfully")