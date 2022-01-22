from datetime import date
import json


def __open_reminders(mode):
    return open('src/db/reminder.json', mode)


def __get_data():
    file = __open_reminders('r')
    data = json.load(file)
    file.close()
    return data


def print_reminders():
    # Se obtienen los datos
    reminders_data = __get_data()
    today = date.today()
    # Formatear fecha
    date_format = today.strftime("%Y/%m/%d")
    # Filtro de recordatorios que se ajusten a la fecha
    reminders_today = list(filter(
        lambda x: x['date'] == date_format,
        reminders_data
    ))
    # Se imprimen los recordatorios
    for reminder in reminders_today:
        print('\n ¡Tienes un recordatorio! \n')
        print(f"{reminder['name']}:")
        print(f" {reminder['description']}\n")
    # Eliminar recordatorios impresos
    if len(reminders_today) > 0:
        reminders = list(filter(
            lambda x: x['date'] != date_format,
            reminders_data
        ))
        file = __open_reminders('w')
        json.dump(reminders, file)
        file.close()
