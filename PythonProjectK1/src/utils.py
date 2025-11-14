import datetime
from typing import Any

import pandas as pd
from pandas import DataFrame


def open_file() -> Any:
    """Функция чтения excel файла"""

    excel_data = pd.read_excel('../data/operations.xlsx', sheet_name='Отчет по операциям')
    return excel_data


def date_filter(date_times: str) -> DataFrame:
    """Функция фильтрует данные excel файла по входящей дате с начала месяца."""

    date_to = datetime.datetime.strptime(date_times, "%Y-%m-%d %H:%M:%S")
    date_from = date_to.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    date_to_str = date_to.strftime("%Y-%m-%d %H:%M:%S")
    date_from_str = date_from.strftime("%Y-%m-%d %H:%M:%S")
    excel_data = open_file()
    excel_data['Дата операции'] = pd.to_datetime(excel_data['Дата операции'], dayfirst=True)
    excel_data_reviews = excel_data.loc[
        (excel_data['Дата операции'] >= date_from_str) &
        (excel_data['Дата операции'] <= date_to_str)]
    sorted_excel_data = excel_data_reviews.sort_values(by='Дата операции', ascending=True)
    return sorted_excel_data

def kart_info(date_fl: DataFrame) -> DataFrame:
    """Функция формирует данные excel файла в формате: последние 4 цифры карты; общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей)."""




if __name__ == '__main__':
    print(date_filter("2021-12-01 23:50:13"))
