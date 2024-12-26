from flask import Flask, render_template, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         date_written TEXT NOT NULL,
         entry_text TEXT NOT NULL,
         feeling INTEGER NOT NULL,
         doctor_comment TEXT)
    ''')
    conn.commit()
    conn.close()

# Initialize the database when the app starts
with app.app_context():
    init_db()

# Routes
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/add_entry')
def add_entry():
    return render_template('add_entry.html')

@app.route('/previous_entries')
def previous_entries():
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    entries = c.execute('SELECT * FROM entries ORDER BY date_written DESC').fetchall()
    conn.close()
    return render_template('previous_entries.html', entries=entries)

# API endpoints
@app.route('/api/entry', methods=['POST'])
def create_entry():
    data = request.json
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO entries (date_written, entry_text, feeling)
        VALUES (?, ?, ?)
    ''', (datetime.now().isoformat(), data['entry_text'], data['feeling']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)