from datetime import date
import pandas as pd
import json

def __open_historical(mode):
    return open('src/db/historical.json', mode)

def __get_data():
    file = __open_historical('r')
    data = json.load(file)
    file.close()
    return data

def get_historical():
    historical_data = __get_data()
    print(pd.DataFrame(historical_data))

def historical(type, message):
    historical_data = __get_data()
    file = __open_historical('w')
    today = date.today()
    date_format = today.strftime("%d/%m/%Y")
    historical_data.append({
        'type': type,
        'change': message,
        'date': date_format
    })
    json.dump(historical_data, file)
    file.close()