# dashboard/app.py
from flask import Flask, render_template, send_from_directory
import json, os
app = Flask(__name__, template_folder="templates", static_folder="static")

DATA_DIR = "../outputs/classroom"
SUMMARY_FILE = os.path.join(DATA_DIR, "classroom_summary.json")

@app.route("/")
def index():
    if not os.path.exists(SUMMARY_FILE):
        return "Run the classroom batch (run_simulation.py -> option 2) first to generate classroom data."
    with open(SUMMARY_FILE) as f:
        summary = json.load(f)
    # prepare data arrays
    identities = [s["identity"] for s in summary]
    wealth = [s["final_wealth"] for s in summary]
    education = [s["final_education"] for s in summary]
    health = [s["final_health"] for s in summary]
    return render_template("index.html", summary=summary, wealth=wealth, education=education, health=health, identities=identities)

@app.route("/student_pdf/<filename>")
def student_pdf(filename):
    # allow download of generated PDFs
    return send_from_directory(DATA_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
