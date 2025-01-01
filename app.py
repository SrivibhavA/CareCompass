from datetime import date
from  flask import *
from classes.journal import Journal
from datetime import datetime

app = Flask(__name__)

USER = 'David'

# Routes
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/get_started' methods = ['GET', 'POST'])
def get_started():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        with open('data/users.txt', 'a') as file:
            file.write(f"{username};{password};{email}")

        global USER
        USER = username

        return redirect(url_for('home'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open('data/users.txt', 'r') as file:
            lines = file.readlines()
            found_match = False
            its = 0
            for line in lines:
                its += 1
                line_content = line.strip().split(':')
                if line_content[0] == username and line_content[1] == password:
                    global USER
                    USER = username
                    found_match = True
                    return redirect(url_for('home'))
            if not found_match and its == len(lines):
                return render_template('login.html', error="Invalid username or password")

        # if username in users and users[username] == password:
        #     return print('success')
        # else:
        #     error = "Invalid username or password"
        #     return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/add_entry')
def add_entry():
    return render_template('add_entry.html')

# API endpoints
@app.route('/add_entry', methods=['POST'])
def create_entry():
    if request.method == 'POST':
        text = request.form['content']  # Get data from input1
        feeling_score = request.form['mood']  # Get data from input2
        journal = Journal(NAME, text, feeling_score, date.today())
        journal.save()
    return redirect(url_for('display_entries'))

@app.route('/previous_entries', methods = ["GET"])
def display_entries():
    entries = get_patient_entries(USER)
    return render_template('previous_entries.html', entries = entries)

@app.route('/doctor_dashboard',  methods = ["GET"])
def doctor_dashboard():
    patients = get_patient_list()
    print("here")
    return render_template('doctor_dashboard.html', patients=patients)


@app.route('/patient/<name>')
def patient_details(name):
    entries = get_patient_entries(name)

    # Prepare data for the feelings graph
    graph_data = []
    for entry in reversed(entries):  # Reverse to show chronological order
        # Convert feeling score to numeric value (1-5)
        feeling_map = {'very sad': 1, 'sad': 2, 'neutral': 3, 'happy': 4, 'very happy': 5}
        feeling_score = feeling_map.get(entry['Feeling Score'].lower(), 3)

        graph_data.append({
            'date': entry['Date'],
            'feeling': feeling_score
        })

    return render_template('patient_details.html',
                           patient_name=name,
                           entries=entries,
                           graph_data=json.dumps(graph_data))


@app.route('/api/add_comment', methods=['POST'])
def add_comment():
    data = request.json
    # In a real application, you would save this to a database
    # For now, we'll just return success
    return jsonify({'status': 'success'})

def parse_entry(line):
    # Parse each line of the text file into a dictionary
    parts = line.strip().split(';')
    entry = {}
    for part in parts:
        key, value = part.split(': ', 1)
        entry[key] = value
    return entry


def read_entries():
    try:
        with open('data/output.txt', 'r') as file:
            entries = [parse_entry(line) for line in file if line.strip()]
        return entries
    except FileNotFoundError:
        return []


def get_patient_list():
    entries = read_entries()
    # Get unique patient names
    patients = list(set(entry['Name'] for entry in entries))
    return sorted(patients)


def get_patient_entries(patient_name):
    entries = read_entries()
    # Filter entries for specific patient
    patient_entries = [entry for entry in entries if entry['Name'] == patient_name]
    # Sort by date
    return sorted(patient_entries, key=lambda x: x['Date'], reverse=True)



if __name__ == '__main__':
    app.run(debug=True)