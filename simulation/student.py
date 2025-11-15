import random

class Student:
    def __init__(self, identity=None):
        self.identity = identity or self.assign_identity()
        self.gender = random.choice(["Male", "Female", "Non-binary"])
        self.background = self.generate_background()
        self.wealth = 50
        self.education = 50
        self.health = 50
        self.history = []  # Track moves and outcomes

    def assign_identity(self):
        identities = ["White", "Black", "Hispanic", "Other"]
        return random.choice(identities)

    def generate_background(self):
        blurbs = {
            "White": "Grew up in a middle-class suburban neighborhood.",
            "Black": "Grew up in an historically redlined area.",
            "Hispanic": "Grew up in an urban neighborhood with limited resources.",
            "Other": "Grew up in a mixed community with variable access to services."
        }
        return blurbs.get(self.identity, "Background unknown.")
