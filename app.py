from datetime import date
from  flask import *
from classes.journal import Journal
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from datetime import datetime
import json

app = Flask(__name__)

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

USER = 'David'

# Routes
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
def home():
    return render_template('home.html')

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

def load_journal_entries():
    entries = []
    with open('data/output.txt', 'r') as file:
        for line in file:
            if line.strip():
                parts = line.strip().split(';')
                name = parts[0].split(': ')[1]
                text = parts[1].split(': ')[1]
                feeling = parts[2].split(': ')[1]
                date = parts[3].split(': ')[1]
                entries.append(Journal(name, text, feeling, date))
    return entries

def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text.lower())

    # Remove stopwords and lemmatize
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    processed_tokens = [
        lemmatizer.lemmatize(token)
        for token in tokens
        if token.isalnum() and token not in stop_words
    ]

    return ' '.join(processed_tokens)

def find_similar_patients(current_patient, entries):
    # Get all texts for current patient
    current_patient_texts = [
        entry.text
        for entry in entries
        if entry.name == current_patient
    ]
    current_patient_text = ' '.join(current_patient_texts)

    # Get unique patients and their combined texts
    unique_patients = {}
    for entry in entries:
        if entry.name != current_patient:
            if entry.name not in unique_patients:
                unique_patients[entry.name] = []
            unique_patients[entry.name].append(entry.text)

    # Calculate similarity scores
    vectorizer = TfidfVectorizer(preprocessor=preprocess_text)
    all_texts = [current_patient_text] + [
        ' '.join(texts) for texts in unique_patients.values()
    ]
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Calculate cosine similarity
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

    # Create result list
    results = []
    for i, (name, texts) in enumerate(unique_patients.items()):
        results.append({
            'name': name,
            'similarity_score': float(similarities[i]),
            'entries': [
                {
                    'text': entry.text,
                    'feeling': entry.feeling_score,
                    'date': entry.date
                }
                for entry in entries
                if entry.name == name
            ]
        })

    # Sort by similarity score
    results.sort(key=lambda x: x['similarity_score'], reverse=True)
    return results



@app.route('/connect')
def connect():
    entries = load_journal_entries()
    unique_patients = list(set(entry.name for entry in entries))
    return render_template('connect.html', patients=unique_patients)


@app.route('/api/similar-patients/<patient_name>')
def get_similar_patients(patient_name):
    entries = load_journal_entries()
    similar_patients = find_similar_patients(patient_name, entries)
    return jsonify(similar_patients)


if __name__ == '__main__':
    app.run(debug=True)