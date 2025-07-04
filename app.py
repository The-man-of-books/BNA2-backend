from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'cars.db'
ADMIN_PIN = '1234'  # Change to your secret PIN!

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                make TEXT,
                model TEXT,
                year INTEGER,
                price REAL,
                image_url TEXT
            )
        ''')
    print("Database initialized.")

@app.route('/cars', methods=['GET'])
def get_cars():
    with sqlite3.connect(DATABASE) as conn:
        cars = conn.execute('SELECT * FROM cars').fetchall()
        cars_list = [
            {"id": row[0], "make": row[1], "model": row[2], "year": row[3], "price": row[4], "image_url": row[5]}
            for row in cars
        ]
    return jsonify(cars_list)

@app.route('/cars', methods=['POST'])
def add_car():
    pin = request.headers.get('Admin-Pin')
    if pin != ADMIN_PIN:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            INSERT INTO cars (make, model, year, price, image_url)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['make'], data['model'], data['year'], data['price'], data['image_url']))
    return jsonify({"message": "Car added successfully."}), 201

@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    pin = request.headers.get('Admin-Pin')
    if pin != ADMIN_PIN:
        return jsonify({"error": "Unauthorized"}), 403

    with sqlite3.connect(DATABASE) as conn:
        conn.execute('DELETE FROM cars WHERE id = ?', (car_id,))
    return jsonify({"message": "Car deleted successfully."})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
