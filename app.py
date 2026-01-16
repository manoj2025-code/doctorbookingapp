from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "database.db"


def get_db():
    return sqlite3.connect(DB_NAME)


@app.route("/")
def index():
    doctors = [
        {"id": 1, "name": "Dr. Anil Kumar", "specialization": "Cardiologist"},
        {"id": 2, "name": "Dr. Priya Sharma", "specialization": "Dermatologist"},
        {"id": 3, "name": "Dr. Ravi Mehta", "specialization": "Orthopedic"},
    ]
    return render_template("index.html", doctors=doctors)


@app.route("/book/<int:doctor_id>", methods=["GET", "POST"])
def book(doctor_id):
    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        time = request.form["time"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO appointments (doctor_id, patient_name, date, time) VALUES (?, ?, ?, ?)",
            (doctor_id, name, date, time),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("appointments"))

    return render_template("book.html", doctor_id=doctor_id)


@app.route("/appointments")
def appointments():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM appointments")
    data = cur.fetchall()
    conn.close()
    return render_template("appointments.html", appointments=data)


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER,
            patient_name TEXT,
            date TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
