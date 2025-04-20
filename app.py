from flask import Flask, render_template, request, jsonify, session, send_file
import os, io, pandas as pd
from data_store import load_user_data, save_user_data
from prompts_db import process_prompt
from pdf_generator import generate_pdf_report
from prompts_db import get_missing_fields

app = Flask(__name__)
app.secret_key = "any-secret-key"

@app.route('/')
def home():
    if 'user' not in session:
        return render_template("index.html", logged_in=False)
    return render_template("index.html", logged_in=True, username=session['user'])

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    session['user'] = username
    if not os.path.exists('users'):
        os.makedirs('users')
    return jsonify({"status": "success", "message": f"Welcome {username}!"})

@app.route('/logout')
def logout():
    session.pop('user', None)
    return jsonify({"status": "logged out"})

@app.route('/message', methods=['POST'])
def handle_message():
    if 'user' not in session:
        return jsonify({"response": "Please login first."})

    msg = request.json['message']
    username = session['user']
    data = load_user_data(username)
    response = process_prompt(msg, data)
    save_user_data(username, data)

    missing = get_missing_fields(data)
    if missing:
        return jsonify({"response": f"{response} \nPlease provide details for: {', '.join(missing)}."})
    else:
        return jsonify({"response": f"{response} \nAll required fields are filled. You can now download the PDF report."})


@app.route('/download_pdf')
def download_pdf():
    if 'user' not in session:
        return "Login required", 403
    username = session['user']
    data = load_user_data(username)
    filename = generate_pdf_report(username, data)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
