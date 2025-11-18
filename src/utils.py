import datetime
import json
import os
from typing import Any, List, Dict

import pandas as pd
import requests
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


def kart_info(date_fl: DataFrame) -> List[Dict]:
    """Функция формирует данные excel файла в формате: последние 4 цифры карты; общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей)."""

    result = []
    fdate_fl = date_fl.fillna('---')

    for index, row in fdate_fl.iterrows():
        if row['Сумма операции'] < 0:
            total_spent = row['Сумма операции с округлением']
            last_digits = str(row['Номер карты'])
            cashback = row['Кэшбэк']
            dict_kart = {'last_digits': last_digits[1:], 'total_spent': total_spent, 'cashback': cashback}
            result.append(dict_kart)
    return result


def top5_transactions(date_fl: DataFrame) -> List[Dict]:
    """Функция Топ-5 транзакций по сумме платежа."""

    result = []
    date_fl.sort_values(by='Сумма платежа', ascending=True, inplace=True)
    for index, row in date_fl[0:5].iterrows():
        dict_top_tr = {"date": row['Дата платежа'],
                       "amount": row['Сумма операции с округлением'],
                       "category": row['Категория'],
                       "description": row['Описание']}
        result.append(dict_top_tr)
    return result


def currency_rates():
    currency = "USD EUR"
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={currency}&base=RUB"
    payload = {}
    headers = {"apikey": "Hzn1ZfOBV2bvKNQBCgsZW72APuJSZI72"}

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    result = response.text
    return result



if __name__ == '__main__':
    print(date_filter("2021-12-01 23:50:13"))
