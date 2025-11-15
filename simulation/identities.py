# simulation/identities.py
import random

IDENTITY_PROFILES = [
    {"race":"White", "gender":"Female", "blurb":"Grew up in a stable neighborhood with family homeownership history."},
    {"race":"White", "gender":"Male",   "blurb":"Family has small business connections; parents had mortgages approved."},
    {"race":"Black", "gender":"Female", "blurb":"Grew up in a community affected by redlining and few local banks."},
    {"race":"Black", "gender":"Male",   "blurb":"Family experienced loan denials; limited generational wealth."},
    {"race":"Hispanic","gender":"Female","blurb":"Recent immigrant family balancing multiple jobs and informal housing."},
    {"race":"Hispanic","gender":"Male","blurb":"Works multiple jobs, limited access to credit history."},
    {"race":"Other","gender":"Nonbinary","blurb":"Diverse background; mixed experiences with access to resources."}
]

def random_identity():
    return random.choice(IDENTITY_PROFILES)
