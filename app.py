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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        pin = request.form.get('pin')
        if pin == '1234567890/.,ManII':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return "Incorrect PIN", 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    with open('cars.json') as f:
        cars = json.load(f)
    return render_template('dashboard.html', cars=cars)

@app.route('/add_car', methods=['POST'])
def add_car():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 403

    # Handle image upload
    image_file = request.files.get('imageFile')
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        timestamp = int(time.time())
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)
        image_url = f"/uploads/{filename}"
    else:
        return "Image upload failed or invalid image.", 400

    # Save car info with image URL
    data = {
        'year': request.form.get('year'),
        'make': request.form.get('make'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'image': image_url
    }

    with open('cars.json', 'r+') as file:
        cars = json.load(file)
        cars.append(data)
        file.seek(0)
        json.dump(cars, file, indent=2)

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0')
