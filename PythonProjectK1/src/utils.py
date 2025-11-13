import datetime
from typing import Any

import pandas as pd
from pandas import DataFrame


def open_file() -> Any:
    """Функция чтения excel файла"""
    excel_data = pd.read_excel('../data/operations.xlsx', sheet_name='Отчет по операциям')
    return excel_data

def info_kart(date_times:str) -> DataFrame:
    date_to = datetime.datetime.strptime(date_times, "%Y-%m-%d %H:%M:%S")
    date_from = date_to.replace(day=1)
    date_to_str = date_to.strftime("%d.%m.%Y %H:%M:%S")
    date_from_str = date_from.strftime("%d.%m.%Y %H:%M:%S")
    excel_data = open_file()
    excel_data['Дата операции'] = pd.to_datetime(excel_data['Дата операции'],dayfirst=True)
    # excel_data = excel_data.set_index('Дата операции')
    # excel_data_range = excel_data.loc[date_from_str:date_to_str]
    print(date_from_str, date_to_str)

    excel_data_reviews = excel_data.loc[(excel_data['Дата операции'] > date_from_str) & (excel_data['Дата операции'] < date_to_str)]

    return excel_data_reviews

print(info_kart("2021-12-19 20:13:13"))
