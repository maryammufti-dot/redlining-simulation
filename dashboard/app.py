from flask import Flask, render_template
import os, json

app=Flask(__name__,template_folder="templates",static_folder="static")

DATA_DIR="../outputs/classroom"
SUMMARY_FILE=os.path.join(DATA_DIR,"classroom_summary.json")

@app.route("/")
def index():
    if not os.path.exists(SUMMARY_FILE):
        return "Run classroom batch (run_simulation.py -> option 2) first."
    with open(SUMMARY_FILE) as f:
        summary=json.load(f)
    identities=[s["identity"] for s in summary]
    wealth=[s["final_wealth"] for s in summary]
    education=[s["final_education"] for s in summary]
    health=[s["final_health"] for s in summary]
    return render_template("index.html",summary=summary,wealth=wealth,education=education,health=health,identities=identities)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
