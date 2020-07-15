import json
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt


def add_new_mode(all_modes):
    """Adds a new mode to the json dictionary

    Args:
        all_modes (dictionary): 

    Returns:
        [type]: [description]
    """
    answer = input("Add the mode that you want to track: \n")
    # Creates a new mode
    all_modes.append({'name':answer, 'date': [], 'high': [], 'low': [],
    'high_acc': [], 'low_acc': []})
    return all_modes[-1]

def add_stats(mode):
    """Adds stats for the current game mode

    Args:
        mode (dictionary): The mode that we want to modify and add to.
    """
    today = date.today()
    if not mode['date']:
        _initialize_new_date(mode)
    elif today.strftime('%Y-%m-%d') != mode["date"][-1]:
        _initialize_new_date(mode)
    
    mode = _input_scores(mode)
    return mode

def _initialize_new_date(mode):
    mode["date"].append(date.today())
    mode['high'].append(0)
    mode['low'].append(99999999)
    mode['high_acc'].append(0)
    mode['low_acc'].append(0)

def _input_scores(mode):
    """A function to input and place scores into the data

    Args:
        mode (dictionary): The mode that we want to modify and add to

    Returns:
        dictionary: a modified dictionary with new values.
    """
    while True:
        try:
            score = float(input('Please put in your score: '))
            acc = float(input('Please put in your accuracy: %'))
            if score > mode["high"][-1]:
                mode['high'][-1] = score
                mode['high_acc'][-1] = acc
            elif score < mode['low'][-1]:
                mode['low'][-1] = score
                mode['low_acc'][-1] = acc
        except ValueError:
            print('Please enter another value.')
        escape = input("Put in more scores? Y/N: ")
        if escape.lower() == 'n':
            break
    return mode

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
        error = "That is not one of the choices. \n"
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

def check_new(full_data):
    """A bool stating whether or not mode_data is a new mode

    full_data(dictionary): a copy of the data.json file
    """
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
            index = 0
    return new_mode

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

new_mode = check_new(full_data)
if new_mode:
    full_data['modes'][index] = add_stats(full_data['modes'][index])

ans = input('Do you want to add scores to this mode for today? Y/N: ')
if ans.lower() == 'y':
    full_data['modes'][index] = add_stats(full_data['modes'][index])

with open(filename, 'w') as f:
    json.dump(full_data, f, default=str)
