from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# -----------------------------
# DATABASE
# -----------------------------
def get_db():
    return sqlite3.connect("database.db")

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            name TEXT,
            status TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            name TEXT,
            rating INTEGER,
            comment TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# HOME PAGE
# -----------------------------
@app.route('/')
def home():
    return render_template('dashboard.html')

# -----------------------------
# SUBMIT RESPONSE
# -----------------------------
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    status = request.form.get('status')

    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO responses VALUES (?, ?)", (name, status))
    conn.commit()
    conn.close()

    return redirect('/admin')   # ✅ redirect to admin

# -----------------------------
# FEEDBACK PAGE
# -----------------------------
@app.route('/feedback')
def feedback_page():
    return render_template('feedback.html')

# -----------------------------
# SUBMIT FEEDBACK
# -----------------------------
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('name')
    rating = request.form.get('rating')
    comment = request.form.get('comment')

    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO feedback VALUES (?, ?, ?)", (name, rating, comment))
    conn.commit()
    conn.close()

    return redirect('/admin')

# -----------------------------
# ADMIN DASHBOARD (IMPORTANT)
# -----------------------------
@app.route('/admin', methods=['GET'])   # ✅ ONLY GET
def admin():
    try:
        conn = get_db()
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM responses WHERE status='yes'")
        eating = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM responses WHERE status='no'")
        not_eating = c.fetchone()[0]

        c.execute("SELECT AVG(rating) FROM feedback")
        avg_rating = c.fetchone()[0]

        c.execute("SELECT * FROM feedback")
        feedbacks = c.fetchall()

        conn.close()

        return render_template(
            'admin.html',
            eating=eating,
            not_eating=not_eating,
            avg_rating=avg_rating if avg_rating else 0,
            feedbacks=feedbacks
        )

    except Exception as e:
        return f"Error: {e}"

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)