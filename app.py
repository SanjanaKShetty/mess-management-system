from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# HOME
@app.route("/")
def home():
    return render_template("dashboard.html")

# SUBMIT
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    status = request.form["status"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            status TEXT
        )
    """)

    cursor.execute("INSERT INTO responses (name, status) VALUES (?, ?)", (name, status))

    conn.commit()
    conn.close()

    return redirect("/")
@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    name = request.form["name"]
    rating = request.form["rating"]
    comment = request.form["comment"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rating INTEGER,
            comment TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO feedback (name, rating, comment) VALUES (?, ?, ?)",
        (name, rating, comment)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")

# ADMIN
@app.route("/admin")
def admin():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Ensure tables exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rating INTEGER,
            comment TEXT
        )
    """)
    

    # Counts
    cursor.execute("SELECT COUNT(*) FROM responses WHERE status='yes'")
    eating = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM responses WHERE status='no'")
    not_eating = cursor.fetchone()[0]

    # Feedback data
    cursor.execute("SELECT name, rating, comment FROM feedback")
    feedbacks = cursor.fetchall()

    # Avg rating
    cursor.execute("SELECT AVG(rating) FROM feedback")
    avg = cursor.fetchone()[0]
    avg_rating = round(avg, 1) if avg else 0

    conn.close()
    

    return render_template(
        "admin.html",
        eating=eating,
        not_eating=not_eating,
        feedbacks=feedbacks,
        avg_rating=avg_rating
    )