from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
import mysql.connector
import bcrypt
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")
CORS(app, supports_credentials=True)

db_config = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASS", ""),
    "database": os.environ.get("DB_NAME", "mealplanner")
}

def get_db():
    return mysql.connector.connect(**db_config)

# Routes for HTML pages
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Registration/Login/Session
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    finally:
        cur.close()
        conn.close()
    return jsonify({"message": "User registered successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

@app.route("/check_session")
def check_session():
    if "user_id" in session:
        return jsonify({"username": session["username"]})
    return jsonify({"error": "Unauthorized"}), 401

# Recommendation
@app.route("/recommend", methods=["POST"])
def recommend():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    disease = data.get("disease")
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT meals.meal_name, meals.description FROM meals JOIN diseases ON meals.disease_id = diseases.id WHERE diseases.name = %s",
        (disease,)
    )
    meals = cur.fetchall()
    cur.close()
    conn.close()
    ai_suggestion = "Try including more fresh vegetables and lean proteins."  # Placeholder for AI
    return jsonify({"meals": meals, "ai": ai_suggestion})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
