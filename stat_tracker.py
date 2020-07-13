import json
from datetime import datetime
import matplotlib.pyplot as plt


def add_new_mode(all_modes):
    answer = input("Add the mode that you want to track: \n")
    all_modes.append({'name':answer})
    return all_modes[-1]

def choose_mode(all_modes):
    """
    Makes the user choose a choice an option from all the modes.
    Args:
        all_modes (Dictionary): All the modes that have been recorded
    """
    while True:
        print("Select a mode: ")
        for value, mode in enumerate(all_modes):
            print(f"{value}: {mode['name']}")
        print(f"{value+1}: Add new mode")
        answer =  int(input())
        error = "That is not one of the choices. \n\
                Please choose from: "
        try:
            if answer == (value+1):
                add_new_mode(all_modes)
                answer = -1
            elif answer < (value+1) and answer >= 0:
                for value, mode in enumerate(all_modes):
                    if answer == value:
                        mode_data = answer
            else: 
                print(error)
                continue
        except ValueError: 
            print(error)
            continue
        break
    return answer

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

# A bool stating whether or not mode_data is a new mode
new_mode = False
if full_data['modes']:
# reads the modes that have already been input and lets the user choose.
    amount_before = len(full_data['modes'])
    index = choose_mode(full_data['modes'])
    if amount_before < len(full_data['modes']):
        new_mode = True
else:
# adds new mode and sets it as default
    add_new_mode(full_data['modes'])
    new_mode = True


with open(filename, 'w') as f:
    json.dump(full_data, f)
