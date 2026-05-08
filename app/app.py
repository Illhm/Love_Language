import os
import json
import uuid
from urllib.parse import quote
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_dev_key_only_change_in_prod')

# Load questions from JSON
with open('app/questions.json', 'r') as f:
    questions = json.load(f)

# The 5 Love Languages
LOVE_LANGUAGES = [
    "Words of Affirmation",
    "Acts of Service",
    "Receiving Gifts",
    "Quality Time",
    "Physical Touch"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET'])
def test():
    # Basic session handling: generate a user ID if none exists
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

    # Check if user has already completed the test
    if session.get('completed'):
        flash("Anda sudah menyelesaikan tes ini. Silakan ulangi tes jika ingin hasil yang baru.")
        return redirect(url_for('result'))

    return render_template('test.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    scores = {lang: 0 for lang in LOVE_LANGUAGES}
    max_score = 30 # Number of questions

    # Process form data
    for q in questions:
        q_id = str(q['id'])
        selected_lang = request.form.get(f'q{q_id}')

        if not selected_lang:
            flash(f"Pertanyaan {q_id} belum dijawab.")
            return redirect(url_for('test'))

        if selected_lang in scores:
            scores[selected_lang] += 1

    # Calculate percentages and rank
    results = []
    for lang, score in scores.items():
        percentage = round((score / max_score) * 100)
        results.append({
            'language': lang,
            'score': score,
            'percentage': percentage
        })

    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)

    # Save to session
    session['results'] = results
    session['completed'] = True

    return redirect(url_for('result'))

@app.route('/result')
def result():
    if 'results' not in session:
        return redirect(url_for('index'))

    results = session['results']
    primary = results[0]

    # Generate WhatsApp Share Link
    app_url = "https://mindsetpsychology.co.id" # Replace with actual domain
    message = f"Hai! Saya baru saja mengikuti Tes Love Language. Bahasa cintaku yang paling dominan adalah *{primary['language']}* ({primary['percentage']}%).\n\nYuk ikutan tesnya juga di sini: {app_url}"
    wa_link = f"https://wa.me/?text={quote(message)}"

    return render_template('result.html', results=results, primary=primary, wa_link=wa_link)

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)