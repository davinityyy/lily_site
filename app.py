from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
import sqlite3
from datetime import datetime

load_dotenv()
DATABASE = os.getenv('DATABASE_PATH', 'diary.db')  # Secure your database path in .env

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    correct_username = "user"
    correct_password = "password123"
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == correct_username and password == correct_password:
            return redirect(url_for('entries'))
        else:
            error = "Invalid username or password. Please try again."
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/diary', methods=['GET', 'POST'])
def diary():
    conn = get_db_connection()
    if request.method == 'POST':
        content = request.form['content']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute('INSERT INTO entries (content, date) VALUES (?, ?)', (content, date))
        conn.commit()
        conn.close()
        return redirect(url_for('entries'))
    return render_template('diary.html')

@app.route('/entries')
def entries():
    conn = get_db_connection()
    entries = conn.execute('SELECT * FROM entries WHERE deleted = 0 ORDER BY date DESC').fetchall()
    conn.close()
    return render_template('entries.html', entries=entries)

@app.route('/entry/<int:id>')
def view_entry(id):
    conn = get_db_connection()
    entry = conn.execute('SELECT * FROM entries WHERE id = ? AND deleted = 0', (id,)).fetchone()
    conn.close()
    return render_template('view_entry.html', entry=entry)

@app.route('/delete/<int:id>')
def delete_entry(id):
    conn = get_db_connection()
    conn.execute('UPDATE entries SET deleted = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('entries'))

@app.route('/logout')
def logout():
    return redirect(url_for('login'))
