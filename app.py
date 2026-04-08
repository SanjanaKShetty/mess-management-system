from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -----------------------------
# DATABASE FUNCTIONS
# -----------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

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
    try:
        name = request.form.get('name')
        status = request.form.get('status')

        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO responses VALUES (?, ?)", (name, status))
        conn.commit()
        conn.close()

        return redirect('/admin')

    except Exception as e:
        return f"Submit Error: {e}"

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
    try:
        name = request.form.get('name')
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO feedback VALUES (?, ?, ?)", (name, rating, comment))
        conn.commit()
        conn.close()

        return redirect('/admin')

    except Exception as e:
        return f"Feedback Error: {e}"

# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
@app.route('/admin')
def admin():
    import sqlite3

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    try:
        # Simple safe queries
        c.execute("SELECT COUNT(*) FROM responses")
        total = c.fetchone()[0]

        c.execute("SELECT * FROM feedback")
        feedbacks = c.fetchall()

    except Exception as e:
        conn.close()
        return f"ERROR: {e}"

    conn.close()

    return f"""
    <h1>Admin Dashboard</h1>
    <p>Total Responses: {total}</p>
    <h2>Feedback:</h2>
    {feedbacks}
    """
# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)