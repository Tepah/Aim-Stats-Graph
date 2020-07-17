import json
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt
# TODO: Clean and refractor a bit

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
    # TODO: Is this working? 
    today = date.today()
    if not mode['date']:
        _initialize_new_date(mode)
    elif today.strftime('%Y-%m-%d') != mode["date"][-1]:
        _initialize_new_date(mode)
    
    mode = _input_scores(mode)
    return mode

def _initialize_new_date(mode):
    """Creates a new date for the mode to add a new high and low

    Args:
        mode (Dictionary): The mode we're adding a new day to
    """
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
            acc = float(input('Please put in your accuracy(%): '))
            if score > mode["high"][-1]:
                mode['high'][-1] = score
                mode['high_acc'][-1] = acc
            if score < mode['low'][-1]:
                mode['low'][-1] = score
                mode['low_acc'][-1] = acc
        except ValueError:
            print('Please enter another value.')
            continue
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

def show_score_graph(full_data, index):
    """Puts information into lists to later put into a graph

    Args:
        full_data (Dictionary): All the data from the json file
        index (int): selects which mode we want to check
    """
    highs =  full_data['modes'][index]['high']
    lows = full_data['modes'][index]['low']
    dates = []
    for date in full_data['modes'][index]['date']:
        try:
            dates.append(datetime.strptime(date, '%Y-%m-%d'))
        except TypeError:
            dates.append(date)

    _plot_graph(highs, lows, dates)

def _plot_graph(highs, lows, dates):
    """Plots the highs and lows in a graph

    Args:
        highs (list): A list of highs
        lows (list): A list of lows
        dates (list): A list of dates
    """
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.plot(dates, highs, c='blue', alpha=0.5)
    ax.plot(dates, lows, c='red', alpha=0.5)
    ax.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

    # Format the plot
    ax.set_title(f"Daily high and low scores for \
        {full_data['modes'][index]['name']}")
    ax.set_xlabel('', fontsize=16)
    fig.autofmt_xdate()
    ax.set_ylabel("Scores", fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize = 16)
    # TODO: How to do hover data points??

    plt.show()

while True:
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
        
    if new_mode:
        full_data['modes'][index] = add_stats(full_data['modes'][index])
    else:
        ans = input('Do you want to add scores to this mode for today? Y/N: ')
        if ans.lower() == 'y':
            full_data['modes'][index] = add_stats(full_data['modes'][index])

    with open(filename, 'w') as f:
        json.dump(full_data, f, default=str)

    ans = input('Do you want to see your chart for highs and lows? Y/N: ')
    if ans.lower() == 'y':
        show_score_graph(full_data, index)

    ans = input("Do you want to continue? Y/N: ")
    if ans.lower() == 'n':
        break
