from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret_key"  # Needed for flash messages

DB_NAME = "students.db"

def init_db():
    """Initializes the database with the students table."""
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                course TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

def get_db_connection():
    """Creates a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        roll = request.form["roll"].strip()
        name = request.form["name"].strip()
        course = request.form["course"].strip()

        if not roll or not name or not course:
            flash("All fields are required!", "error")
            return redirect(url_for("add_student"))

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO students (roll, name, course) VALUES (?, ?, ?)", (roll, name, course))
            conn.commit()
            flash("Student added successfully!", "success")
            return redirect(url_for("view_students")) # Redirect to view after adding
        except sqlite3.IntegrityError:
            flash("Error: Roll Number already exists!", "error")
        finally:
            conn.close()

    return render_template("add.html")

@app.route("/view")
def view_students():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("view.html", students=students)

@app.route("/search", methods=["GET", "POST"])
def search_student():
    student = None
    message = None
    if request.method == "POST":
        roll = request.form["roll"].strip()
        conn = get_db_connection()
        student = conn.execute("SELECT * FROM students WHERE roll = ?", (roll,)).fetchone()
        conn.close()
        if not student:
            message = "Student not found."
    
    return render_template("search.html", student=student, message=message)

@app.route("/delete/<roll>")
def delete_student(roll):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE roll = ?", (roll,))
    conn.commit()
    conn.close()
    flash("Student deleted successfully!", "success")
    return redirect(url_for("view_students"))

if __name__ == "__main__":
    init_db()  # Initialize DB on start
    app.run(debug=True)
