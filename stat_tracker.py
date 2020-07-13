import json
from datetime import datetime
import matplotlib.pyplot as plt

# read the data file into the system
filename = 'data/aim_data.json'
try:
    with open(filename) as f:
        full_data = json.load(f)
except FileNotFoundError:
    # creates the data file if none is found.
    full_data = {'modes':[]}
    with open(filename, 'w') as f:
        json.dump(full_data, f)

if full_data['modes']:
    # reads the modes that have already been input and lets the user choose.
    print("Select mode you want to add to: ")
    for value, mode in enumerate(full_data['modes']):
        print(f"{value} {mode['type']}")
    print(f"{value+1} add new mode")
    answer =  input()
else:
    add_new_mode()

with open(filename, 'w') as f:
    json.dump(full_data, f)

def add_new_mode():
    answer = input("Add the mode that you want to track: \n")
    full_data['modes'].append({'type':answer})