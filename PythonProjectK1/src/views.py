import datetime
from typing import Any


def home_page(date_times:str) ->Any:
    """Функция формирует JSON файл с данными для главной страницы"""

    date_obj = datetime.datetime.strptime(date_times, "%Y-%m-%d %H:%M:%S")
    hour = date_obj.hour
    if 0 < hour < 5:
        greetings = 'Доброй ночи'
    elif 5 < hour < 11:
        greetings = 'Доброе утро'
    elif 11 < hour < 18:
        greetings = 'Добрый день'
    else:
        greetings = 'Добрый вечер'

    return greetings

