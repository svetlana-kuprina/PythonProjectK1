import datetime
import json
import logging
import os
from typing import Any, Dict

from src.utils import date_filter, kart_info, top5_transactions, currency_rates, stock_price, open_file

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
log_directory = os.path.join(os.path.dirname(__file__), "../logs", "utils.log")
file_handler = logging.FileHandler(log_directory, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def home_page(date_times: str) -> Dict[str, Any]:
    """Функция формирует JSON файл с данными для главной страницы.
    Принимает на вход строку с датой и временем открытия, типа 2021-12-19 20:13:13"""

    try:
        date_to = datetime.datetime.strptime(date_times, "%Y-%m-%d %H:%M:%S")
        hour = date_to.hour
        excel_data_fr = open_file()
        date_excel_filter = date_filter(date_times, excel_data_fr)
        cards = kart_info(date_excel_filter)
        top_transactions = top5_transactions(date_excel_filter)
        currency_r = currency_rates()
        stock_price_result = stock_price()
        if stock_price_result != [] or currency_r != []:
            logger.info("Успешно получена информация от API по курсам валют и акциям")

        if 0 < hour < 5:
            greetings = "Доброй ночи"
        elif 5 < hour < 11:
            greetings = "Доброе утро"
        elif 11 < hour < 18:
            greetings = "Добрый день"
        else:
            greetings = "Добрый вечер"
        data = {
            "greetings": greetings,
            "cards": cards,
            "top_transactions": top_transactions,
            "currency_rates": currency_r,
            "stock_price": stock_price_result,
        }
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        logger.info("Успешно сформирован JSON-ответ")
    except Exception as ex:
        logger.error(f"Ошибка {ex}")
    return json_data
#
#
# if __name__ == "__main__":
#     date_times = "2021-12-02 20:13:13"
#     print(home_page(date_times))
