# simulation/events.py
import random

# Life events and choices
LIFE_EVENTS = [
    {"id":"housing", "event":"You want to buy a house in your neighborhood.",
     "choices":["Apply for mortgage","Rent instead","Move to another area"]},
    {"id":"college", "event":"You want to go to college.",
     "choices":["Apply for scholarships","Attend community college","Skip college"]},
    {"id":"health_minor", "event":"You need healthcare for a minor illness.",
     "choices":["Go to private clinic","Go to community clinic","Ignore symptoms"]},
    {"id":"job_offer", "event":"You are offered a job opportunity.",
     "choices":["Take high paying job","Take moderate paying job","Start own business"]},
    {"id":"car", "event":"You want to buy a car.",
     "choices":["Apply for auto loan","Buy used car with cash","Take public transportation"]},
    {"id":"business", "event":"You want to start a small business.",
     "choices":["Apply for business loan","Self-fund business","Wait and save money"]},
    {"id":"medical_emergency", "event":"You face a medical emergency.",
     "choices":["Go to ER","Visit urgent care","Ignore symptoms"]},
    {"id":"promotion", "event":"You are up for a promotion.",
     "choices":["Promotion awarded","Promotion delayed","No promotion"]},
    {"id":"childcare", "event":"You need childcare for your child.",
     "choices":["Affordable high-quality childcare","Moderate childcare","Rely on family/friends"]},
    {"id":"safety", "event":"You are concerned about neighborhood safety.",
     "choices":["Safe neighborhood","Moderate safety","Unsafe neighborhood"]}
]

# Outcome probabilities by race
OUTCOME_RULES = {
    "mortgage": {
        "White": (0.05,0.15,0.80),
        "Black": (0.50,0.30,0.20),
        "Hispanic": (0.35,0.40,0.25),
        "Other": (0.25,0.45,0.30)
    },
    "scholarship": {
        "White": (0.05,0.20,0.75),
        "Black": (0.40,0.35,0.25),
        "Hispanic": (0.30,0.45,0.25),
        "Other": (0.20,0.50,0.30)
    },
    "auto loan": {
        "White": (0.05,0.20,0.75),
        "Black": (0.40,0.40,0.20),
        "Hispanic": (0.30,0.45,0.25),
        "Other": (0.20,0.50,0.30)
    },
    "business loan": {
        "White": (0.10,0.25,0.65),
        "Black": (0.45,0.35,0.20),
        "Hispanic": (0.35,0.40,0.25),
        "Other": (0.25,0.45,0.30)
    },
    "promotion": {
        "White": (0.05,0.15,0.80),
        "Black": (0.40,0.35,0.25),
        "Hispanic": (0.30,0.45,0.25),
        "Other": (0.25,0.50,0.25)
    },
    "health": {
        "White": (0.05,0.20,0.75),
        "Black": (0.30,0.40,0.30),
        "Hispanic": (0.25,0.45,0.30),
        "Other": (0.20,0.50,0.30)
    },
    "default": {
        "White": (0.05,0.20,0.75),
        "Black": (0.35,0.40,0.25),
        "Hispanic": (0.30,0.45,0.25),
        "Other": (0.25,0.50,0.25)
    }
}

OUTCOME_EFFECTS = {
    "Denied": (-5,-3,-5),
    "Partial": (3,4,-1),
    "Success": (10,8,5)
}

def resolve_outcome(race, choice):
    key = choice.lower()
    if "mortgage" in key:
        rule = OUTCOME_RULES["mortgage"]
    elif "scholarship" in key:
        rule = OUTCOME_RULES["scholarship"]
    elif "auto loan" in key:
        rule = OUTCOME_RULES["auto loan"]
    elif "business loan" in key:
        rule = OUTCOME_RULES["business loan"]
    elif "promotion" in key:
        rule = OUTCOME_RULES["promotion"]
    elif "clinic" in key or "er" in key or "health" in key:
        rule = OUTCOME_RULES["health"]
    else:
        rule = OUTCOME_RULES["default"]
    probs = rule.get(race, OUTCOME_RULES["default"][race])
    r = random.random()
    if r < probs[0]:
        return "Denied"
    elif r < probs[0]+probs[1]:
        return "Partial"
    else:
        return "Success"
