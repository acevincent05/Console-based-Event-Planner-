import json #local database
import uuid #event identification
import datetime #date and time formatting

events_data = 'events_data.json' #file of the data stored in the same folder

events = {} #nested dictionary where the events are placed and accessed

def write_data():   #writes data in the 'events_data.json' file
    global events_data, events  #gives the program global access to the saved data
    with open(events_data, "w") as file:
        json.dump(events, file, indent=4)

def load_data(): #reads data in the 'events_data.json' file
    global events_data, events
    with open(events_data, "r") as file:
        events = json.load(file)

def file_handler(): #generates the json file if the file doesn't exist
    try:
        load_data()
    except FileNotFoundError:
        write_data()

def format_date(input_date): #formats the date entered by the user
    try:
        date_object = datetime.datetime.strptime(input_date, "%m-%d-%Y")
        formatted_date = date_object.strftime("%A, %B %d, %Y").replace(" 0", " ")
        return formatted_date
    except ValueError:
        return "invalid"

def format_time(input_time): #formats the time entered by the user
    try:
        time_object = datetime.datetime.strptime(input_time, "%I:%M")
        formatted_time = time_object.strftime("%I:%M").lstrip('0')
        return formatted_time
    except ValueError:
        return "invalid"

def sched_event():  #user add events

    file_handler()

    event_id = str(uuid.uuid1())
    event_name = input('Enter the name of the event: ')
    while True:
        input_date = input('Enter the date of the event (MM-DD-YYYY): ')
        event_date = format_date(input_date)    
        if event_date == 'invalid':
            print('Invalid date input.')
        else:
            break
    while True:
        input_time = input('Enter the time of the event (HH:MM): ')
        event_time = format_time(input_time)
        if event_time == 'invalid':
            print('Invalid time input.')
        else:
            break
    while True:
        event_daytime = input('Select AM or PM: ').upper()
        if event_daytime == 'AM' or event_daytime == 'PM':
            break
        else:
            print('Invalid input.')

    events[event_id] = {"name" : event_name, 
                        "date": event_date, 
                        "time" : event_time, 
                        "day_time" : event_daytime}

    write_data()

    print('\nEvent successfully added!')

def view_events():  #user views the saved events
    file_handler()

    if len(events) == 0:
        print('\n-----------------------------------------')
        print('\nNo events added.\n')
        print('-----------------------------------------')
    else:
        print('\n-----------------------------------------')
        print('------------| ADDED EVENTS |-------------')
        print('-----------------------------------------')

        for event_id, details in events.items():
            print(f'\nID: {event_id}')
            print(f'\nEvent: {details['name']}')
            print(f'Date: {details['date']}')
            print(f'Time: {details['time']} {details['day_time']}\n')
            print('-----------------------------------------')

def edit_events():  #user edits the saved events
    file_handler()
    if len(events) == 0:
        print('\n-----------------------------------------')
        print('\nNo existing events to delete.\n')
        print('-----------------------------------------')
    else:
        while True:
            event_id = input('Enter event ID: ')
            if event_id in events:
                new_event_name = input(f'Edit event name "{events[event_id]['name']}": ')
                while True:
                    input_date = input(f'Edit event date "{events[event_id]['date']}" (MM-DD-YYYY): ')
                    new_event_date = format_date(input_date)
                    if new_event_date == 'invalid':
                        print('Invalid date input.')
                    else:
                        break
                while True:
                    input_time = input(f'Edit event time "{events[event_id]['time']}" (HH:MM): ')
                    new_event_time = format_time(input_time)
                    if new_event_time == 'invalid':
                        print('Invalid time input.')
                    else:
                        break
                while True:
                    new_event_daytime = input('Select AM or PM: ').upper()
                    if new_event_daytime == 'AM' or new_event_daytime == 'PM':
                        break
                    else:
                        print('invalid input')

                events[event_id] = {"name" : new_event_name,
                                    "date": new_event_date,
                                    "time" : new_event_time,
                                    "day_time" : new_event_daytime}

                with open(events_data, "w") as file:
                    json.dump(events, file, indent=4)

                print('\nEvent succesfully edited!')
                break
            else:
                print('Invalid event ID.')

def delete_event(): #user edits events by entering the event ID
    file_handler()
    if len(events) == 0:
        print('\n-----------------------------------------')
        print('\nNo existing events to delete.\n')
        print('-----------------------------------------')
    else:
        event_id = input('Select an event to delete: ')
        del events[event_id]
        print('Event succesfully deleted.')

    write_data()

def menu(): #allows the user navigate the main functions of the program
    print('\n-----------------------------------------')
    print('------------| EVENT PLANNER |------------')
    print('-----------------------------------------')
    print('1. Schedule an event')
    print('2. View added events')
    print('3. Edit an event')
    print('4. Delete an event')
    print('5. Exit')
    
    menu_input = input('\nEnter option: ')
    
    if menu_input == '1':
        sched_event()
    elif menu_input == '2':
        view_events()
    elif menu_input == '3':
        edit_events()
    elif menu_input == '4':
        delete_event()
    elif menu_input == '5':
        quit()
    else:
        print('Invalid input.')

def back_menu(): #gives users an option to return to the main menu or exit the program
    while True:
        print('\n1. Return to main menu')
        print('2. Exit')
        return_menu = input('\nEnter option: ').upper()
        if return_menu == '1':
            menu()
        elif return_menu == '2':
            break
        else:
            print('Invalid input.')

menu() #program starts with the main menu displayed
back_menu() #return to main menu or exit the program