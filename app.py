from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"
DATABASE = "hw13.db"

conn = sqlite3.connect("hw13.db")
with open("schema.sql") as f:
    conn.executescript(f.read())
conn.commit()
conn.close()
print("Database initialized.")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Root route
@app.route("/")
def index():
    return redirect(url_for("login"))

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "password":
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    db = get_db()
    students = db.execute("SELECT * FROM students").fetchall()
    quizzes = db.execute("SELECT * FROM quizzes").fetchall()
    return render_template("dashboard.html", students=students, quizzes=quizzes)

# Add Student
@app.route("/student/add", methods=["GET", "POST"])
def add_student():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        db = get_db()
        db.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)",
                   (request.form["first_name"], request.form["last_name"]))
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("add_student.html")

# Delete Student
@app.route('/student/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    db = get_db()
    db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    db.execute("DELETE FROM results WHERE student_id = ?", (student_id,))
    db.commit()
    return redirect(url_for('dashboard'))

# Add Quiz
@app.route("/quiz/add", methods=["GET", "POST"])
def add_quiz():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        db = get_db()
        db.execute("INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)",
                   (request.form["subject"], request.form["num_questions"], request.form["quiz_date"]))
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("add_quiz.html")

# Delete Quiz
@app.route('/quiz/<int:quiz_id>/delete', methods=['POST'])
def delete_quiz(quiz_id):
    db = get_db()
    db.execute("DELETE FROM quizzes WHERE id = ?", (quiz_id,))
    db.execute("DELETE FROM results WHERE quiz_id = ?", (quiz_id,))
    db.commit()
    return redirect(url_for('dashboard'))

# Student Results
@app.route("/student/<int:student_id>")
def student_results(student_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    db = get_db()
    results = db.execute("""
        SELECT results.quiz_id, results.score, quizzes.subject, quizzes.quiz_date
        FROM results
        JOIN quizzes ON results.quiz_id = quizzes.id
        WHERE results.student_id = ?
    """, (student_id,)).fetchall()
    return render_template("student_results.html", results=results, student_id=student_id)

# Add Result
@app.route("/results/add", methods=["GET", "POST"])
def add_result():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    db = get_db()
    students = db.execute("SELECT * FROM students").fetchall()
    quizzes = db.execute("SELECT * FROM quizzes").fetchall()
    if request.method == "POST":
        db.execute("INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)",
                   (request.form["student_id"], request.form["quiz_id"], request.form["score"]))
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("add_result.html", students=students, quizzes=quizzes)

@app.route('/result/<int:result_id>/delete', methods=['POST'])
def delete_result(result_id):
    db = get_db()
    db.execute("DELETE FROM results WHERE id = ?", (result_id,))
    db.commit()
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=True)
