from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

BACKEND_URL = 'http://localhost:5001'

@app.route('/api', methods=['GET'])
def get_users():
    response = requests.get(BACKEND_URL + '/api')
    if response.ok:
        users = response.json()
    else:
        flash("Could not fetch users")
        users = []
    return render_template('users.html', users=users)

@app.route('/simple_form', methods=['GET', 'POST'])
def simple_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        response = requests.post(BACKEND_URL + '/simple_form_submit', json={
            'name': name,
            'email': email,
            'password': password
        })

        if response.status_code == 201:
            return redirect(url_for('success'))
        else:
            error = response.json().get('error', 'Unknown error')
            flash(f"An error occurred: {error}")
            return render_template('simpleForm.html')

    return render_template('simpleForm.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
