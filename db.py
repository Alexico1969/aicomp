import sqlite3, os
from flask import g
from urllib import parse

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

def init_db():
    cursor.execute("CREATE TABLE IF NOT EXISTS assignments (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, level TEXT)")
    return "Database initialized"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('mydatabase.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db():
    if 'db' in g:
        g.db.close()

def get_assignments():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM assignments")
    assignments = cursor.fetchall()
    return assignments

def add_assignment(name, description, level):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO assignments (name, description, level) VALUES (?, ?, ?)", (name, description, level))
    db.commit()
    return "Assignment added"

def delete_assignment(name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM assignments WHERE name=?", (name,))
    db.commit()
    return "Assignment deleted"