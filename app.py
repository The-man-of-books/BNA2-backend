from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_from_directory
from flask_cors import CORS
import json
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # Secret key for session
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper: Check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Admin Login
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        pin = request.form.get('pin')
        if pin == '1234':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return "Incorrect PIN", 401
    return render_template('login.html')

# Admin Dashboard
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    with open('cars.json') as f:
        cars = json.load(f)
    return render_template('dashboard.html', cars=cars)

# Add Car Route (Supports both JSON and Form)
@app.route('/add-car', methods=['POST'])
def add_car():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 403

    if request.is_json:
        data = request.get_json()
    else:
        # From traditional form submission
        data = {
            'name': request.form.get('carName'),
            'price': request.form.get('price'),
            'image': request.form.get('image')
        }

    with open('cars.json', 'r+') as file:
        cars = json.load(file)
        cars.append(data)
        file.seek(0)
        json.dump(cars, file, indent=2)

    # Redirect back to dashboard if form submitted
    if not request.is_json:
        return redirect(url_for('dashboard'))

    return jsonify({'message': 'Car added successfully!'}), 200

# Logout Route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

# Upload Image Route (Safe Upload)
@app.route('/upload', methods=['POST'])
def upload_image():
    image_file = request.files.get('imageFile')
    image_url = request.form.get('imageUrl')

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        # Add timestamp to avoid filename clashes
        timestamp = int(time.time())
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)
        image_url = f"/uploads/{filename}"
    elif image_url:
        # Provided external URL (assuming trusted source)
        pass
    else:
        return jsonify({'error': 'Invalid or no image provided'}), 400

    return jsonify({'imageUrl': image_url})

# Serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0')
