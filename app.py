from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        pin = request.form.get('pin')
        if pin == '1234':
            return redirect(url_for('dashboard'))
        else:
            return "Incorrect PIN", 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    with open('cars.json') as f:
        cars = json.load(f)
    return render_template('dashboard.html', cars=cars)

@app.route('/add-car', methods=['POST'])
def add_car():
    data = request.json
    with open('cars.json', 'r+') as file:
        cars = json.load(file)
        cars.append(data)
        file.seek(0)
        json.dump(cars, file, indent=2)
    return jsonify({'message': 'Car added successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
