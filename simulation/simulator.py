# simulation/simulator.py
from .identities import random_identity
from .events import LIFE_EVENTS, resolve_outcome, OUTCOME_EFFECTS
import random
import time

class Student:
    def __init__(self):
        prof = random_identity()
        self.identity = prof["race"]
        self.gender = prof["gender"]
        self.blurb = prof["blurb"]
        self.wealth = 50
        self.education = 50
        self.health = 50
        self.history = []  # list of (event_id,event_text,choice,outcome,effects,timestamp)

    def record(self, event_id, event_text, choice, outcome):
        effects = OUTCOME_EFFECTS[outcome]
        self.wealth += effects[0]
        self.education += effects[1]
        self.health += effects[2]
        self.history.append({
            "time": time.time(),
            "event_id": event_id,
            "event": event_text,
            "choice": choice,
            "outcome": outcome,
            "effects": effects,
            "wealth": self.wealth,
            "education": self.education,
            "health": self.health
        })

def run_interactive(student=None):
    if student is None:
        student = Student()
    print(f"Assigned identity: {student.identity} ({student.gender})")
    print(student.blurb)
    events = LIFE_EVENTS.copy()
    random.shuffle(events)  # ensure no repeats
    for ev in events:
        print("\nEVENT:")
        print(ev["event"])
        for i, ch in enumerate(ev["choices"],1):
            print(f"{i}. {ch}")
        while True:
            try:
                pick = int(input("Enter the number of your choice: "))
                if 1 <= pick <= len(ev["choices"]):
                    break
                print("Invalid choice number.")
            except ValueError:
                print("Enter a number.")
        choice = ev["choices"][pick-1]
        outcome = resolve_outcome(student.identity, choice)
        student.record(ev["id"], ev["event"], choice, outcome)
        print(f"Outcome: {outcome}")
        # show updated status
        print(f"Status: Wealth={student.wealth}, Education={student.education}, Health={student.health}")
    return student
