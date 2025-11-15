# run_simulation.py
from simulation.simulator import run_interactive, Student
from simulation.export_utils import export_csv, export_pdf, export_map
import json, os

def single_run():
    s = run_interactive()
    csvfile = export_csv(s)
    pdffile = export_pdf(s)
    print(f"\nSaved CSV: {csvfile}")
    print(f"Saved PDF: {pdffile}")
    # Optional small neighborhood map (demo data)
    neighborhood = {"lat":42.33,"lon":-83.03,"spots":[{"lat":42.34,"lon":-83.02,"label":"Grocery A"}]}
    mapfile = export_map(neighborhood)
    print(f"Saved map: {mapfile}")

def classroom_run(n=30, outdir="outputs/classroom"):
    os.makedirs(outdir, exist_ok=True)
    students = []
    for i in range(n):
        s = Student()
        # run deterministic short sim (random events no input) for classroom demo
        from simulation.events import LIFE_EVENTS
        import random
        events = LIFE_EVENTS.copy()
        random.shuffle(events)
        for ev in events:
            # choose default best personal choice (1) but outcome resolved by identity to simulate
            choice = ev["choices"][0]
            from simulation.events import resolve_outcome
            outcome = resolve_outcome(s.identity, choice)
            s.record(ev["id"], ev["event"], choice, outcome)
        students.append(s)
        export_csv(s, path=outdir)
        export_pdf(s, path=outdir)
    print(f"Classroom run complete. {n} students saved to {outdir}")
    # Save a summary JSON for dashboard
    summary = []
    for s in students:
        summary.append({
            "identity": s.identity,
            "gender": s.gender,
            "final_wealth": s.wealth,
            "final_education": s.education,
            "final_health": s.health
        })
    with open(os.path.join(outdir,"classroom_summary.json"), "w") as f:
        json.dump(summary, f)
    print("Saved classroom_summary.json")

if __name__ == "__main__":
    print("Redlining Simulation - choose mode:")
    print("1. Single interactive student")
    print("2. Classroom batch run (30 students)")
    mode = input("Enter 1 or 2: ").strip()
    if mode == "1":
        single_run()
    else:
        classroom_run()
