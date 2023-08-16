import json

with open("vectors.json", "r") as f:
    vecs = json.load(f)

for k, v in vecs.items():
    test = ''
