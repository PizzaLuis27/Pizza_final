import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Verbindung zur SQLite-Datenbank erstellen
def get_db_connection():
    conn = sqlite3.connect("database.db")  # Erstellt die Datei database.db
    conn.row_factory = sqlite3.Row
    return conn

import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Zeitintervalle von 11:30 bis 13:30 in 10-Minuten-Schritten
time_slots = {time: "green" for time in ["11:30", "11:40", "11:50", "12:00", "12:10", "12:20",
                                         "12:30", "12:40", "12:50", "13:00", "13:10", "13:20", "13:30"]}

# Speichere Buchungen
bookings = {}
ADMIN_PASSWORD = "Pizza27"


@app.route('/')
def index():
    return render_template('index.html', time_slots=time_slots, bookings=bookings)


@app.route("/order", methods=["POST"])
def order():
    data = request.json
    name = data["name"]
    pizzas = data["pizzas"]
    time = data["time"]

    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO orders (name, pizzas, time) VALUES (?, ?, ?)", (name, pizzas, time))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False  # Falls der Slot schon gebucht ist
    conn.close()

    return jsonify({"success": success})



@app.route("/")
def index():
    conn = get_db_connection()
    orders = conn.execute("SELECT time FROM orders").fetchall()
    conn.close()

    # Liste mit gebuchten Zeiten erstellen
    booked_times = {order["time"] for order in orders}
    return render_template("book.html", orders=booked_times)



@app.route('/cancel', methods=['POST'])
def cancel():
    data = request.json
    password = data.get('password')
    time = data.get('time')

    if password != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Falsches Passwort!"})

    if time in bookings:
        del bookings[time]
        time_slots[time] = "green"
        return jsonify({"status": "success", "message": "Reservierung storniert!"})

    return jsonify({"status": "error", "message": "Reservierung nicht gefunden!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pizzas INTEGER NOT NULL,
            time TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

# Tabelle beim Start erstellen
create_table()


