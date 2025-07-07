
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_from_directory
from flask_cors import CORS
import json
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Utility: Check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Utility: Load cars from JSON
def load_cars(file_path='cars.json'):
    if not os.path.exists(file_path):
        return []
    with open(file_path) as f:
        return json.load(f)

# Utility: Save cars to JSON
def save_cars(cars, file_path='cars.json'):
    with open(file_path, 'w') as f:
        json.dump(cars, f, indent=2)

# Routes for handling the functionality (you can modify or extend based on your needs)
@app.route('/')
def index():
    cars = load_cars()
    return render_template('index.html', cars=cars)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "File uploaded successfully"}), 200
    return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
