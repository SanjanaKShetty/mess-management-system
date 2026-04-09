from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------------- DB ----------------
def get_db():
    conn = sqlite3.connect("database.db")
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        status TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        rating INTEGER,
        comment TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("dashboard.html")

# ---------------- SUBMIT MEAL ----------------
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    status = request.form.get("status")

    conn = get_db()
    conn.execute("INSERT INTO responses (name, status) VALUES (?, ?)", (name, status))
    conn.commit()
    conn.close()

    return redirect("/")

# ---------------- FEEDBACK PAGE ----------------
@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

# ---------------- SUBMIT FEEDBACK ----------------
@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    name = request.form.get("name")
    rating = request.form.get("rating")
    comment = request.form.get("comment")

    if not rating:
        return "Please select rating ⭐"

    conn = get_db()
    conn.execute(
        "INSERT INTO feedback (name, rating, comment) VALUES (?, ?, ?)",
        (name, int(rating), comment)
    )
    conn.commit()
    conn.close()

    return redirect("/admin")

# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    conn = get_db()

    eating = conn.execute("SELECT COUNT(*) FROM responses WHERE status='yes'").fetchone()[0]
    not_eating = conn.execute("SELECT COUNT(*) FROM responses WHERE status='no'").fetchone()[0]

    feedbacks = conn.execute("SELECT name, rating, comment FROM feedback").fetchall()

    avg = conn.execute("SELECT AVG(rating) FROM feedback").fetchone()[0]
    avg_rating = round(avg, 1) if avg else 0

    conn.close()

    return render_template(
        "admin.html",
        eating=eating,
        not_eating=not_eating,
        feedbacks=feedbacks,
        avg_rating=avg_rating
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)