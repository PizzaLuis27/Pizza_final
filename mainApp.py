from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

orders = {}
ADMIN_PASSWORD = "1234"


@app.route("/")
def index():
    time_slots = {f"{h:02d}:{m:02d}": "red" if f"{h:02d}:{m:02d}" in orders else "green"
                  for h in range(11, 14) for m in range(0, 60, 10)}
    return render_template("index.html", time_slots=time_slots)


@app.route("/book", methods=["POST"])
def book():
    data = request.json
    time = data["time"]
    if time in orders:
        return jsonify({"status": "error", "message": "Zeit bereits reserviert!"})

    orders[time] = {"name": data["name"], "pizzas": data["pizzas"], "contact": data["contact"]}
    return jsonify({"status": "success", "message": "Reservierung erfolgreich!"})


@app.route("/admin", methods=["POST"])
def admin():
    data = request.json
    if data["password"] == ADMIN_PASSWORD:
        return jsonify({"status": "success", "bookings": orders})
    return jsonify({"status": "error", "message": "Falsches Passwort!"})


if __name__ == "__main__":
    app.run(debug=True)
