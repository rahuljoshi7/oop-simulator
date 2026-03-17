from flask import Flask, render_template, request, redirect, session
from config import Config
from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import json

# ================= APP INIT =================
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
app.permanent_session_lifetime = timedelta(days=7)

# ================= IMPORT MODELS (IMPORTANT) =================
from models.user import User
from models.quiz_result import QuizResult

# ================= CREATE TABLES (PRODUCTION FIX) =================
with app.app_context():
    db.create_all()

# ================= LOAD QUESTIONS =================
def load_questions():
    with open("questions/beginner.json") as f:
        beginner = json.load(f)

    with open("questions/intermediate.json") as f:
        intermediate = json.load(f)

    with open("questions/advanced.json") as f:
        advanced = json.load(f)

    return {
        "beginner": beginner,
        "intermediate": intermediate,
        "advanced": advanced
    }

quiz_data = load_questions()

# ================= HOME =================
@app.route("/")
def home():
    return redirect("/login")

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session.permanent = True
            session["user_id"] = user.id
            session["user_name"] = user.name
            return redirect("/dashboard")

        return "Invalid email or password"

    return render_template("login.html")

# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        new_user = User(name=name, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html", name=session["user_name"])

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================= SIMULATOR =================
@app.route("/simulator", methods=["GET", "POST"])
def simulator():

    if "user_id" not in session:
        return redirect("/login")

    if "objects" not in session:
        session["objects"] = []

    class_name = session.get("class_name")
    attributes = session.get("attributes")

    if request.method == "POST":

        # Create class
        if request.form.get("class_name") and request.form.get("attributes"):
            class_name = request.form["class_name"]
            attributes = request.form["attributes"]

            session["class_name"] = class_name
            session["attributes"] = attributes
            session["objects"] = []

        # Create object
        elif request.form.get("object_name") and request.form.get("values"):

            object_name = request.form["object_name"]
            values = request.form["values"]

            if attributes:
                attr_list = [a.strip() for a in attributes.split(",")]
                value_list = [v.strip() for v in values.split(",")]

                object_map = dict(zip(attr_list, value_list))

                objects = session.get("objects", [])
                objects.append({
                    "object_name": object_name,
                    "mapping": object_map
                })

                session["objects"] = objects

    result = None
    if class_name and attributes:
        result = {
            "class_name": class_name,
            "attributes": [a.strip() for a in attributes.split(",")]
        }

    return render_template(
        "simulator.html",
        result=result,
        objects=session.get("objects", [])
    )

# ================= RESET =================
@app.route("/reset")
def reset():
    session.pop("class_name", None)
    session.pop("attributes", None)
    session.pop("objects", None)
    return redirect("/simulator")

# ================= QUIZ =================
@app.route("/quiz/<level>", methods=["GET", "POST"])
def quiz(level):

    if "user_id" not in session:
        return redirect("/login")

    questions = quiz_data.get(level)

    if not questions:
        return "Invalid level"

    if request.method == "POST":

        score = 0
        results = []

        for i, q in enumerate(questions):

            user_answer = request.form.get(f"q{i}")
            correct_answer = q["correct"]

            is_correct = user_answer == correct_answer

            if is_correct:
                score += 1

            results.append({
                "question": q["question"],
                "selected": user_answer,
                "correct": correct_answer,
                "is_correct": is_correct,
                "explanation": q["explanation"]
            })

        total = len(questions)
        percentage = (score / total) * 100

        # Save result
        new_result = QuizResult(
            user_id=session["user_id"],
            level=level,
            score=score,
            total=total,
            percentage=percentage
        )

        db.session.add(new_result)
        db.session.commit()

        session["last_score"] = score
        session["last_total"] = total
        session["last_level"] = level

        return redirect("/next-level")

    return render_template("quiz.html", questions=questions, topic=level)

# ================= NEXT LEVEL =================
@app.route("/next-level")
def next_level():

    score = session.get("last_score")
    total = session.get("last_total")
    level = session.get("last_level")

    percentage = (score / total) * 100

    if level == "beginner":
        next_lvl = "intermediate" if percentage >= 60 else "beginner"

    elif level == "intermediate":
        next_lvl = "advanced" if percentage >= 60 else "intermediate"

    else:
        next_lvl = "advanced"

    return render_template(
        "progress.html",
        score=score,
        total=total,
        percentage=percentage,
        next_level=next_lvl
    )

# ================= PERFORMANCE =================
@app.route("/performance")
def performance():

    if "user_id" not in session:
        return redirect("/login")

    results = QuizResult.query.filter_by(user_id=session["user_id"]).all()

    return render_template("performance.html", results=results)


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)