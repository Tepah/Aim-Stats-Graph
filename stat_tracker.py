import json
from datetime import datetime
import matplotlib.pyplot as plt

# read the data file into the system
filename = 'data/aim_data.json'
try:
    with open(filename) as f:
        full_data = json.load(f)
except FileNotFoundError:
    full_data = {}
    with open(filename, 'w') as f:
        json.dump(full_data, f)