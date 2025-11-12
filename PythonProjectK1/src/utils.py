import datetime
from typing import Any

import pandas as pd


def open_file() -> Any:
    """Функция чтения excel файла"""
    excel_data = pd.read_excel('../data/operations.xlsx')
    return excel_data

def time_range(date_times):
    """Функция обработки времени"""

    date_obj = datetime.datetime.strptime(date_times, "%Y-%m-%d %H:%M:%S")
    date_obj =
    date_from = date_obj.replace(day=1)


    return date_from, date_to

def info_kart():
    pass
print(time_range('2024-05-14 16:35:27'))