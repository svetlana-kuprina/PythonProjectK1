import datetime
import json
import logging
import os
from typing import Any, List, Dict
from venv import logger

import pandas as pd
import requests
from pandas import DataFrame

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
log_directory = os.path.join(os.path.dirname(__file__), "../logs", "utils.log")
file_handler = logging.FileHandler(log_directory, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def open_file() -> Any:
    """Функция чтения excel файла"""

    try:
        excel_data = pd.read_excel('../data/operations.xlsx', sheet_name='Отчет по операциям')
        logger.info('Успешное чтение файла excel')
    except FileNotFoundError:
        logger.error('Файл с настройками пользователя не найден')
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
    logger.info('Успешный отбор по дате')
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
    logger.info('Успешный вывод данных по операциям')
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
    logger.info('Успешный вывод данных Топ-5 транзакций')
    return result


def currency_rates() -> List[Dict]:
    """Функция запроса курса валют"""
    try:
        result = []
        dict_result = {}
        path_json = os.path.join('../data/user_settings.json')
        with open(path_json) as json_file:
            user_settings = json.load(json_file)
            user_currencies = user_settings['user_currencies']
            print(user_currencies)
        for row in user_currencies:
            url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={row}"
            payload = {}
            headers = {"apikey": "Hzn1ZfOBV2bvKNQBCgsZW72APuJSZI72"}
            response = requests.request("GET", url, headers=headers, data=payload)
            response.raise_for_status()
            response_data = response.json()
            dict_result["currency"] = row
            dict_result['rates'] = response_data['rates']['RUB']
            result.append(dict_result)
    except FileNotFoundError:
        logger.error('Файл с настройками пользователя не найден')
    except requests.exceptions.HTTPError:
        logger.error(f'Ошибка связи с API')
    except json.decoder.JSONDecodeError:
        logger.error('')

    return result


if __name__ == '__main__':
    print(date_filter("2021-12-01 23:50:13"))
