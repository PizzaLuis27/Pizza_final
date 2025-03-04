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


@app.route('/book', methods=['POST'])
def book():
    data = request.json
    time = data.get('time')
    name = data.get('name')
    pizzas = data.get('pizzas')
    contact = data.get('contact')
    if time_slots.get(time) == "red":
        return jsonify({"status": "error", "message": "Dieses Feld wurde schon reserviert!"})

    time_slots[time] = "red"
    bookings[time] = {"name": name, "pizzas": pizzas, "contact": contact}  # Fix: contact wird jetzt gespeichert

    return jsonify({"status": "success", "message": "Reservierung erfolgreich!"})


@app.route('/admin', methods=['POST'])
def admin():
    data = request.json
    password = data.get('password')

    if password != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Falsches Passwort!"})

    return jsonify({"status": "success", "bookings": bookings})


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

