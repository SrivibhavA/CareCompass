from datetime import date
from flask import *
from classes.journal import Journal
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

# @app.route('/previous_entries')
# def previous_entries():
#     conn = sqlite3.connect('journal.db')
#     c = conn.cursor()
#     entries = c.execute('SELECT * FROM entries ORDER BY date_written DESC').fetchall()
#     conn.close()
#     return render_template('previous_entries.html', entries=entries)

# API endpoints
@app.route('/add_entry', methods=['POST'])
def create_entry():
    if request.method == 'POST':
        text = request.form['content']  # Get data from input1
        feeling_score = request.form['mood']  # Get data from input2
        journal = Journal(text, feeling_score, date.today())
        journal.save()
    return redirect(url_for('display_entries'))

@app.route('/previous_entries', methods = ["GET"])
def display_entries():
    entries = []
    with open("output.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            entry_info = line.strip().split(";")
            entries.append(entry_info)
            print(entries)
    return render_template('previous_entries.html', entries = entries)
        

if __name__ == '__main__':
    app.run(debug=True)