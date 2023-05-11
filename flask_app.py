
from os import getenv, environ
from flask import Flask, render_template, session, request, redirect, url_for, g
from db import init_db, get_db, close_db, get_assignments, add_assignment, delete_assignment, get_filtered_assignments
import random


app=Flask(__name__, static_url_path='/static')

init_db()

app.secret_key = 'Bruce Wayne is Batman'

@app.route('/', methods=['GET', 'POST'])
def home_page():
    title = "?"
    description = "<br><br><br>"

    if request.method == 'POST':
        level = request.form['level']
        print(f"Level: {level}")
        assignments = get_filtered_assignments(level)
        random_assignment = random.choice(assignments)
        title = random_assignment[1]
        description = random_assignment[2]


    return render_template('home.html', title=title, description=description)

@app.route('/login', methods=['GET', 'POST'])
def login():
   return "login"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
   return "signup"

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('home_page'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if request.method == 'POST':
        try:
            action = request.form['action']
            if action[:3] == "Del":
                print(f"Deleting {action[9:]}")
                delete_assignment(action[9:])
            else:
                name = request.form['name']
                description = request.form['description']
                level = request.form['level']
                add_assignment(name, description, level)
        except:
            print("Error adding assignment")
            pass
       
    assignments = get_assignments()

    return render_template('admin.html', assignments=assignments)

@app.route('/admin_delete/<name>', methods=['GET', 'POST'])
def admin_delete(name):
    delete_assignment(name)
    return f"Deleted assignment {name}"



# Do not alter this if statement below
# This should stay towards the bottom of this file
if __name__ == "__main__":
    flask_env = getenv('FLASK_ENV')
    if flask_env != 'production':
        environ['FLASK_ENV'] = 'development'
        app.debug = True
        app.asset_debug = True
        server = Server(app.wsgi_app)
        server.serve()
    app.run()

