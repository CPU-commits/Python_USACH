import pandas as pd
import json
import datetime

from utils import utils
from historical import historical

def __open_reminders(mode):
    return open('src/db/reminder.json', mode)

def __get_data():
    file = __open_reminders('r')
    data = json.load(file)
    file.close()
    return data

def __print_instructions():
    print('\n Instrucciones: \n')
    print('Al momento de crear un recordatorio, estos van a ser almacenados')
    print('Serán mostrados al ejecutar el programa y la fecha coincida la fecha indicada')
    print('Posterior a su recordatorio, serán completamente eliminados')

def __show_reminder():
    reminders_data = __get_data()
    print(pd.DataFrame(reminders_data))

def __validate_date():
    menu_open = True
    while menu_open:
        reminder_date = input('Fecha del recordatorio (Formato: YYYY/MM/DD): ')
        message = 'Fecha no válida'
        if '/' not in reminder_date:
            print(message)
        else:
            split_date = reminder_date.split('/')
            if len(split_date) != 3:
                print(message)
            else:
                if len(split_date[0]) != 4 or utils.is_num(split_date[0]) == False:
                    print(message)
                elif len(split_date[1]) != 2 or utils.is_num(split_date[1]) == False:
                    print(message)
                elif len(split_date[2]) != 2 or utils.is_num(split_date[2]) == False:
                    print(message)
                else:
                    try:
                        datetime.datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]))
                        menu_open = False
                    except ValueError:
                        print(message)
    return reminder_date

def __create_reminder():
    reminder_name = input('Nombre del recordatorio: ')
    reminder_description = input('Descripción del recordatorio: ')
    reminder_date = __validate_date()
    reminders_data = __get_data()
    reminders_file = __open_reminders('w')
    reminders_data.append({
        'name': reminder_name,
        'description': reminder_description,
        'date': reminder_date,
    })
    json.dump(reminders_data, reminders_file)
    historical.historical('Insertar', 'Se inserta recordatorio')
    reminders_file.close()

def reminders():
    menu_open = True
    while menu_open:
        print('1) Crear un recordatorio')
        print('2) Ver recordatorios')
        print('3) Instrucciones')
        print('4) Retroceder')
        option = input('Escoga una opción: ')
        if option == '1':
            __create_reminder()
        elif option == '2':
            __show_reminder()
        elif option == '3':
            __print_instructions()
        elif option == '4':
            menu_open = False
        else:
            print('Escoga una opción válida')