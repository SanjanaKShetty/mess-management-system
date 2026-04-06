import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

students = []

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    name = request.form['name']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM meals WHERE status='yes'")
    count = cursor.fetchone()[0]

    conn.close()

    return render_template('dashboard.html', name=name, count=count)

@app.route('/submit', methods=['POST'])
def submit():
    status = request.form['status']
    name = request.form.get('name', 'Anonymous')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO meals (name, status) VALUES (?, ?)", (name, status))

    conn.commit()
    conn.close()

    return "Response Saved in Database!"
@app.route('/feedback_page/<name>')
def feedback_page(name):
    return render_template('feedback.html', name=name)


@app.route('/feedback', methods=['POST'])
def feedback():
    name = request.form['name']
    rating = request.form['rating']
    comment = request.form['comment']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO feedback (name, rating, comment) VALUES (?, ?, ?)",
                   (name, rating, comment))

    conn.commit()
    conn.close()

    return "Feedback Submitted!"
@app.route('/admin')
def admin():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Total eating
    cursor.execute("SELECT COUNT(*) FROM meals WHERE status='yes'")
    eating = cursor.fetchone()[0]

    # Total not eating
    cursor.execute("SELECT COUNT(*) FROM meals WHERE status='no'")
    not_eating = cursor.fetchone()[0]

    # Average rating
    cursor.execute("SELECT AVG(rating) FROM feedback")
    avg_rating = cursor.fetchone()[0]

    # All feedback
    cursor.execute("SELECT name, rating, comment FROM feedback")
    feedbacks = cursor.fetchall()

    conn.close()

    return render_template('admin.html',
                           eating=eating,
                           not_eating=not_eating,
                           avg_rating=avg_rating,
                           feedbacks=feedbacks)

if __name__ == "__main__":
    app.run()