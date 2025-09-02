from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = "supersecretkey"
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5000"])

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "mealplanner"
}

def get_db():
    return mysql.connector.connect(**db_config)

# ----- Serve HTML pages -----
@app.route("/")
def index():
    return send_from_directory("template", "index.html")  # serve login/register page

@app.route("/dashboard")
def dashboard():
    return send_from_directory("template", "mealplanner.html")  # serve dashboard

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
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/check_session", methods=["GET"])
def check_session():
    if "user_id" in session:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT username FROM users WHERE id = %s", (session["user_id"],))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"username": user["username"]})
    else:
        return jsonify({"error": "Not logged in"}), 401
    
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})

@app.route("/recommend", methods=["POST"])
def recommend():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    disease = data.get("disease")

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT meals.meal_name, meals.description FROM meals JOIN diseases ON meals.disease_id = diseases.id WHERE diseases.name = %s", (disease,))
    meals = cur.fetchall()
    cur.close()
    conn.close()

    ai_suggestion = f"For {disease}, focus on balanced meals, hydration, and regular exercise."

    if not meals:
        return jsonify({"message": "No meals found for this condition", "ai": ai_suggestion, "meals": []})
    return jsonify({"meals": meals, "ai": ai_suggestion})


@app.route("/verify_payment/<reference>")
def verify_payment(reference):
    headers = {
        "Authorization": "sk_test_016e04f4b2e897ee6f40f249a4126e01dcbc91d3"
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    resp = request.get(url, headers=headers)
    data = resp.json()
    if data["status"] == True and data["data"]["status"] == "success":
        # Update user as premium in your DB
        return jsonify({"message": "Payment verified successfully"})
    return jsonify({"error": "Payment verification failed"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
