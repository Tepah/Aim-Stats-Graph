import json
from datetime import datetime
import matplotlib.pyplot as plt


def add_new_mode(all_modes, new_mode):
    answer = input("Add the mode that you want to track: \n")
    all_modes.append({'name':answer})
    new_mode = True
    return full_data['modes'][-1]

def choose_mode(all_modes, new_mode):
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
                mode_data = add_new_mode(all_modes, new_mode)
            elif answer > (value+1) and answer < 0:
                for value, mode in enumerate(all_modes):
                    if answer == value:
                        mode_data = mode[answer]
            else: 
                print(error)
                continue
        except ValueError: 
            print(error)
            continue
        break
    return mode_data

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
    mode_data = choose_mode(full_data['modes'], new_mode)
else:
# adds new mode and sets it as default
    mode_data = add_new_mode(full_data['modes'], new_mode)

if new_mode:
    print("new_mode changed")

with open(filename, 'w') as f:
    json.dump(full_data, f)
