import datetime
import json
from typing import Any, Dict

from src.utils import date_filter, kart_info


def home_page(date_times:str) ->Dict[str,Any]:
    """Функция формирует JSON файл с данными для главной страницы. Принимает на вход строку с датой и временем открытия,
    типа 2021-12-19 20:13:13"""

    date_to = datetime.datetime.strptime(date_times, "%Y-%m-%d %H:%M:%S")
    date_from = date_to.replace(day=1)
    hour = date_to.hour
    if 0 < hour < 5:
        greetings = 'Доброй ночи'
    elif 5 < hour < 11:
        greetings = 'Доброе утро'
    elif 11 < hour < 18:
        greetings = 'Добрый день'
    else:
        greetings = 'Добрый вечер'
    data = {
        "greetings": greetings
    }
    json_data = json.dumps(data,ensure_ascii=False, indent=4)
    date_excel_filter= date_filter(date_times)
    kart = kart_info(date_excel_filter)


    return json_data

if __name__ == '__main__':
    date_times = "2021-12-19 20:13:13"
    print(home_page(date_times))

