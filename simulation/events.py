# simulation/events.py
# Branching storylines & scenario definitions.
# All identities are presented the same CHOICES, but outcomes differ by identity.
import random

# Life events (10) — choices identical for everyone
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

# Outcome probabilities and effects by (race)
# For each important choice keyword, define outcome chances for different races.
OUTCOME_RULES = {
    # keyword in choice: mapping race -> probabilities for ("Denied","Partial","Success")
    "mortgage": {
        "White": (0.05, 0.15, 0.80),
        "Black": (0.50, 0.30, 0.20),
        "Hispanic": (0.35, 0.40, 0.25),
        "Other": (0.25, 0.45, 0.30)
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
    # Generic groups (health, general)
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

def _pick_rule(choice_text):
    text = choice_text.lower()
    if "mortgage" in text:
        return OUTCOME_RULES["mortgage"]
    if "scholarship" in text:
        return OUTCOME_RULES["scholarship"]
    if "auto loan" in text:
        return OUTCOME_RULES["auto loan"]
    if "business loan" in text:
        return OUTCOME_RULES["business loan"]
    if "promotion" in text:
        return OUTCOME_RULES["promotion"]
    if "clinic" in text or "er" in text or "health" in text:
        return OUTCOME_RULES["health"]
    return OUTCOME_RULES["default"]

def resolve_outcome(identity_race, choice_text):
    rule = _pick_rule(choice_text)
    probs = rule.get(identity_race, rule["default"]) if isinstance(rule, dict) else rule[identity_race]
    # probs is (p_denied, p_partial, p_success)
    r = random.random()
    if r < probs[0]:
        return "Denied"
    elif r < probs[0] + probs[1]:
        return "Partial"
    else:
        return "Success"

# Effects mapping by outcome: (wealth_delta, education_delta, health_delta)
OUTCOME_EFFECTS = {
    "Denied": ( -5, -3, -5),
    "Partial": ( 3, 4, -1),
    "Success": ( 10, 8, 5)
}
