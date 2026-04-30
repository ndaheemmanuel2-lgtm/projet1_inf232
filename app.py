from flask import Flask, render_template, request, jsonify, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prenom TEXT,
        nom TEXT,
        matricule TEXT,
        age INTEGER,
        sexe TEXT,
        note REAL
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- LOGIN ----------------
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    user = request.form["user"]
    pwd = request.form["pwd"]

    if user == "admin" and pwd == "admin":
        session["user"] = user
        return redirect("/dashboard")

    return "Login incorrect"

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html")

# ---------------- API GET ----------------
@app.route("/api/students", methods=["GET"])
def get_students():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "prenom": r[1],
            "nom": r[2],
            "matricule": r[3],
            "age": r[4],
            "sexe": r[5],
            "note": r[6]
        })
    return jsonify(data)

# ---------------- API ADD ----------------
@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.json

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO students(prenom, nom, matricule, age, sexe, note)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["prenom"],
        data["nom"],
        data["matricule"],
        data["age"],
        data["sexe"],
        data["note"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "ajouté"})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=False)
