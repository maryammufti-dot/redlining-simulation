# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from simulation.identities import random_identity
from simulation.events import LIFE_EVENTS, resolve_outcome, OUTCOME_EFFECTS
import random, time, threading

app = Flask(__name__)
CORS(app)

# Classroom state (in-memory)
classroom_state = {}  # student_id -> data
MAX_STUDENTS = 35

lock = threading.Lock()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/start_student", methods=["POST"])
def start_student():
    with lock:
        if len(classroom_state) >= MAX_STUDENTS:
            return jsonify({"error":"Classroom full"}), 403
        student_id = str(time.time())  # simple unique ID
        prof = random_identity()
        classroom_state[student_id] = {
            "identity": prof["race"],
            "gender": prof["gender"],
            "blurb": prof["blurb"],
            "wealth":50,
            "education":50,
            "health":50,
            "history": [],
            "current_event_index":0
        }
    return jsonify({"student_id":student_id,
                    "identity":prof["race"],
                    "gender":prof["gender"],
                    "blurb":prof["blurb"]})

@app.route("/get_next_event/<student_id>", methods=["GET"])
def get_next_event(student_id):
    student = classroom_state.get(student_id)
    if not student: return jsonify({"error":"Student not found"}), 404
    idx = student["current_event_index"]
    if idx >= len(LIFE_EVENTS):
        return jsonify({"done":True})
    event = LIFE_EVENTS[idx]
    return jsonify({"done":False,"event":event})

@app.route("/submit_move", methods=["POST"])
def submit_move():
    data = request.json
    student_id = data.get("student_id")
    choice = data.get("choice")
    student = classroom_state.get(student_id)
    if not student: return jsonify({"error":"Student not found"}),404
    idx = student["current_event_index"]
    if idx >= len(LIFE_EVENTS):
        return jsonify({"done":True})
    event = LIFE_EVENTS[idx]
    outcome = resolve_outcome(student["identity"], choice)
    effects = OUTCOME_EFFECTS[outcome]
    student["wealth"] += effects[0]
    student["education"] += effects[1]
    student["health"] += effects[2]
    student["history"].append({
        "event":event["event"],
        "choice":choice,
        "outcome":outcome,
        "effects":effects
    })
    student["current_event_index"] += 1
    return jsonify({"next_index":student["current_event_index"], "outcome":outcome})

@app.route("/get_dashboard")
def get_dashboard():
    return jsonify(classroom_state)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
