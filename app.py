from flask import Flask

app = Flask(__name__)

@app.route('/admin')
def admin():
    conn = sqlite3.connect("database.db")
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

if __name__ == "__main__":
    app.run(debug=True)