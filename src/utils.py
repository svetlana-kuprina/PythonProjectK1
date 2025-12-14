import datetime
import json
import logging
import os
from typing import List, Dict


import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame

load_dotenv()

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
log_directory = os.path.join(os.path.dirname(__file__), "../logs", "utils.log")
file_handler = logging.FileHandler(log_directory, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def open_file() -> DataFrame:
    """Функция чтения excel файла"""

    try:
        path_file = os.path.join(os.path.dirname(__file__), "../data", "operations.xlsx")
        excel_data = pd.read_excel(path_file, sheet_name="Отчет по операциям")
        logger.info("Успешное чтение файла excel")
    except FileNotFoundError:
        logger.error("Файл с транзакциями не найден")
        return pd.DataFrame({})
    except Exception as error:
        logger.error(error)
        return pd.DataFrame({})

    return excel_data


def date_filter(date_times: str, excel_data) -> DataFrame:
    """Функция фильтрует данные excel файла по входящей дате с начала месяца."""

    try:
        date_to = datetime.datetime.strptime(date_times, "%Y-%m-%d %H:%M:%S")
        date_from = date_to.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        date_to_str = date_to.strftime("%Y-%m-%d %H:%M:%S")
        date_from_str = date_from.strftime("%Y-%m-%d %H:%M:%S")
        excel_data["Дата операции"] = pd.to_datetime(excel_data["Дата операции"], dayfirst=True)
        excel_data_reviews = excel_data.loc[
            (excel_data["Дата операции"] >= date_from_str) & (excel_data["Дата операции"] <= date_to_str)
        ]
        sorted_excel_data = excel_data_reviews.sort_values(by="Дата операции", ascending=True)
        logger.info("Успешный отбор по дате")
    except ValueError:
        logger.error("Не верный формат даты")
    except KeyError:
        logger.error("Данные файла operations.xlsx не соответствуют формату")

    return sorted_excel_data


def kart_info(date_fl: DataFrame) -> List[Dict]:
    """Функция формирует данные excel файла в формате: последние 4 цифры карты; общая сумма расходов; кешбэк."""

    try:
        result = []
        fdate_fl = date_fl.fillna("---")

        for index, row in fdate_fl.iterrows():
            if row["Сумма операции"] < 0:
                total_spent = row["Сумма операции с округлением"]
                last_digits = str(row["Номер карты"])
                cashback = row["Кэшбэк"]
                dict_kart = {"last_digits": last_digits[1:], "total_spent": total_spent, "cashback": cashback}
                result.append(dict_kart)
        logger.info("Успешный вывод данных по операциям")
    except Exception as error:
        logger.error(error)
        return []
    return result


def top5_transactions(date_fl: DataFrame) -> List[Dict]:
    """Функция Топ-5 транзакций по сумме платежа."""

    result = []
    date_fl.sort_values(by="Сумма платежа", ascending=True, inplace=True)
    for index, row in date_fl[0:5].iterrows():
        dict_top_tr = {
            "date": row["Дата платежа"],
            "amount": row["Сумма операции с округлением"],
            "category": row["Категория"],
            "description": row["Описание"],
        }
        result.append(dict_top_tr)
    logger.info("Успешный вывод данных Топ-5 транзакций")
    return result


def open_user_settings():
    try:
        path_json = os.path.join(os.path.dirname(__file__), "../data", "user_settings.json")
        with open(path_json) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        logger.error("Файл с настройками пользователя не найден")
        return []
    except Exception as error:
        logger.error(error)
        return []


def currency_rates(user_set) -> List[Dict]:
    """Функция запроса курса валют"""

    try:
        result = []
        user_currencies = user_set["user_currencies"]
        for row in user_currencies:
            dict_result = {}
            url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={row}"
            payload = {}
            headers = {"apikey": os.getenv("APIKEY")}
            response = requests.get(url, headers=headers, data=payload)

            response.raise_for_status()
            response_data = response.json()
            dict_result["currency"] = row
            dict_result["rates"] = round(response_data["rates"]["RUB"], 2)
            result.append(dict_result)
    except requests.exceptions.HTTPError:
        logger.error(f"Ошибка связи с API Ошибка {response.status_code}")
        return result
    except json.decoder.JSONDecodeError:
        logger.error("Ошибка связи с API")
        return result
    except requests.exceptions.ConnectionError:
        logger.error("Ошибка связи. Нет соединения с сайтом. Проверьте подключение к сети")
        return result
    except Exception as error:
        logger.error(error)
        return result

    return result


def stock_price(user_set):
    """Функция запроса Стоимости акций из S&P500 по настройкам пользовательского файла"""

    try:
        result = []

        user_stocks = user_set["user_stocks"]
        for row in user_stocks:
            dict_result = {}
            headers_api = {"apikey": os.getenv("APIKEY2")}
            url1 = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={row}&apikey={headers_api}"
            r = requests.get(url1)
            r.raise_for_status()
            data = r.json()
            dict_result["stock"] = row
            dict_result["rates"] = data["Global Quote"]["02. open"]
            result.append(dict_result)
    except requests.exceptions.HTTPError as error:
        logger.error(f"Ошибка связи с API Ошибка {error}")
    except json.decoder.JSONDecodeError as error:
        logger.error(f"Ошибка связи с API {error}")
    except KeyError as err:
        logger.error(
            f"Ошибка {err} Возможно закончился лимит подключения к API."
            " Проверьте возможность подключения на сайте https://www.alphavantage.co/"
        )
    except requests.exceptions.ConnectionError as er:
        logger.error(f"Ошибка связи {er}. Нет соединения с сайтом. Проверьте подключение к сети")
        return result

    return result
