from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("dashboard.html")

# Submit form
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    status = request.form["status"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO responses (name, status) VALUES (?, ?)", (name, status))
    conn.commit()
    conn.close()

    return redirect("/")

# Admin page
@app.route("/admin")
def admin():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM responses WHERE status='yes'")
    eating = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM responses WHERE status='no'")
    not_eating = cursor.fetchone()[0]

    cursor.execute("SELECT name, status FROM responses")
    data = cursor.fetchall()

    conn.close()

    return render_template("admin.html",
                           eating=eating,
                           not_eating=not_eating,
                           data=data)

if __name__ == "__main__":
    app.run(debug=True)