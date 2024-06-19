
from flask import Flask, render_template, redirect, url_for, request, session, flash, Response, jsonify
from datetime import datetime
import os
import sqlite3
import io
import re
from lib.models.studenten import Studentennummer
from lib.models.login import Login
from lib.models.statements import Statements
from lib.models.teacher import Teacher
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) # added a secret key for session
    
# Home
@app.route("/")
def show_home():
    # clear the session
    #session.clear()
    if 'authenticated_teacher' in session and session['authenticated_teacher'] is not None and session['authenticated_teacher'] == True:
        return redirect("/teachers/read")
    else:
        session['authenticated_teacher'] = False
        return render_template("home.html")

@app.route("/teachers/logout")
def logout():
    # clear the session
    session.clear()
    return redirect("/")

@app.route("/vragenlijst/vragen",  methods=["GET", "POST"])
def vragenlijst():
    if 'authenticated_teacher' in session and session['authenticated_teacher'] is not None and session['authenticated_teacher'] == True:
        return redirect("/teachers/read")
    else:
        session['authenticated_teacher'] = False
        if request.method == 'POST' and 'studentennummer' in request.form:
                output = Studentennummer.check_student(request.form['studentennummer'])
                print(output)
                if output == False:
                    return jsonify({'output':output})
                else:
                    session['studentennummer'] = output[2]
                    session['naam'] = output[3]
                    session['klas'] = output[4]
                    session['last_completed_statement'] = output[1]
                    return jsonify({'output':output})
        elif request.method == 'POST' and 'statementnumber' in request.form:
            output_instert_statements = Statements.instert_statements(session['studentennummer'], request.form['statementnumber'], request.form['value'])
            session['last_completed_statement'] = output_instert_statements
            return jsonify({'output':output_instert_statements})
        
        elif request.method == 'POST' and 'action_type' in request.form and request.form['action_type'] == 'klaar':
            output_get_code = Studentennummer.get_code(request.form['studentnummer'])
            return jsonify({'output':output_get_code})
        
        elif request.method == 'POST' and 'action_type' in request.form and request.form['action_type'] == 'opnieuw':
            output_opnieuw = Studentennummer.opnieuw(request.form['studentnummer'])
            session['last_completed_statement'] = 0
            return jsonify({'output':output_opnieuw})

        return render_template("vragenlijst/vragen.html")

@app.route("/teachers/login",  methods=["GET", "POST"])
def login():
    if 'authenticated_teacher' in session and session['authenticated_teacher'] is not None and session['authenticated_teacher'] == True:
        return redirect("/teachers/read")
    else:
        if request.method == 'POST':
            return_login = Login.login(request.form['Email'], request.form['Wachtwoord'])
            print(return_login[0])
            if return_login[0] == True:
                session['authenticated_teacher'] = True
                session['teacher_name'] = return_login[1]
                if return_login[2] == True:
                    session['is_admin'] = True
                else:
                    session['is_admin'] = False
                return jsonify({'output':return_login[0]})
            else:
                return jsonify({'output':return_login[1]})
        return render_template("teachers/login.html")

@app.route("/teachers/read",  methods=["GET", "POST"])
def show_all():
    print("ïn show all")
    if 'authenticated_teacher' in session and session['authenticated_teacher'] is not None and session['authenticated_teacher'] == True:
        print(session['teacher_name'])
        student_list = Studentennummer.read()
        active_page = request.args.get('page', 1, type=int) # get the page number from the url
        items_per_page = 10
        start_index = (active_page - 1) * items_per_page
        end_index = start_index + items_per_page
        total_pages = len(student_list) // items_per_page + 1
        student_to_display = student_list[start_index:end_index]

        if request.method == 'POST' and 'action_type' in request.form and request.form['action_type'] == 'add':
            output = Studentennummer.check_student(request.form['studentennummer'], request.form['naam'], request.form['klas'])
            return jsonify({'output':output[1]})
            
        elif request.method == 'POST' and 'type' in request.form and request.form['type'] == 'get_for_edit':
            print(request.form['studentnummer'])
            output = Studentennummer.get_for_edit(request.form['studentnummer'])
            return jsonify({'output':output})
        
        elif request.method == 'POST' and 'action_type' in request.form and request.form['action_type'] == 'edit':
            output = Studentennummer.update_student(request.form['studentennummer'], request.form['naam'], request.form['klas'])
            return jsonify({'output':output})

        elif request.method == 'POST' and 'action_type' in request.form and request.form['action_type'] == 'delete':
            print("welkom in delete")
            output = Studentennummer.delete_student(request.form['studentennummer'])
            return jsonify({'output':output})

        return render_template("teachers/read.html", student_list=student_to_display , total_pages=total_pages, active_page=active_page)
    else:
        return redirect("/")
    
@app.route("/teachers/read_admin",  methods=["GET", "POST"])
def show_all_teachers():
    if 'authenticated_teacher' in session and session['authenticated_teacher'] is not None and 'is_admin' in session  and session['is_admin'] == True and session['authenticated_teacher'] == True:
        teacher_list = Teacher.read()
        active_page = request.args.get('page', 1, type=int) # get the page number from the url
        items_per_page = 10
        start_index = (active_page - 1) * items_per_page
        end_index = start_index + items_per_page
        total_pages = len(teacher_list) // items_per_page + 1
        teacher_list_to_display = teacher_list[start_index:end_index]

        if request.method == 'POST' and 'action_type' in request.form and request.form['action_type'] == 'add':
            output = Teacher.add_teacher(request.form['email'], request.form['naam'], request.form['password'], request.form.get('is_admin'))
            return jsonify({'output':output[1]})
            
        elif request.method == 'POST' and 'type' in request.form and request.form['type'] == 'get_for_edit':
            print(request.form['teacher_id'])
            output = Teacher.get_for_edit(request.form['teacher_id'])
            return jsonify({'output':output})
        
        elif request.method == 'POST' and 'action_type' in request.form and request.form['action_type'] == 'edit':
            output = Teacher.update_teacher(request.form['teacher_id'], request.form['naam'], request.form['email'], request.form.get('is_admin'))
            return jsonify({'output':output})

        elif request.method == 'POST' and 'action_type' in request.form and request.form['action_type'] == 'delete':
            output = Teacher.delete_teacher(request.form['teacher_id'])
            return jsonify({'output':output})

        return render_template("teachers/read_admin.html", teacher_list=teacher_list_to_display , total_pages=total_pages, active_page=active_page)
    else:
        return redirect("/")

# Runs the app locally in debug mode
if __name__ == '__main__':
    app.run(debug = True)
