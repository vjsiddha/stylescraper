from flask import Flask, request, render_template
import json
import spacy
import os
import subprocess

app = Flask(__name__)

def ensure_spacy_model():
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm")
    return nlp

nlp = ensure_spacy_model()

def process_query(query):
    doc = nlp(query)
    return [token.lemma_ for token in doc if not token.is_stop]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    processed_query = process_query(query)

    # Load the scraped data
    with open(os.path.join('fashionscraper', 'fashionscraper', 'spiders', 'items.json'), 'r') as f:
        items = json.load(f)

    # Filter the items based on the query
    results = [item for item in items if any(token.lower() in item['name'].lower() for token in processed_query)]

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
