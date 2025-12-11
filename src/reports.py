import datetime
import logging
import os
from typing import Optional

import dateutil
import pandas as pd

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
log_directory = os.path.join(os.path.dirname(__file__), "../logs", "utils.log")
file_handler = logging.FileHandler(log_directory, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция формирования отчета, возвращает траты по заданной категории за последние три месяца"""
    try:
        if date is None:
            date_t = datetime.date.today()
            date_f = date_t - datetime.timedelta(days=90)
            date_to = date_t.strftime("%d-%m-%Y")
            date_from = date_f.strftime("%d-%m-%Y")
        else:
            date_t = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            date_f = date_t - datetime.timedelta(days=90)
            date_to = date_t.strftime("%Y-%m-%d %H:%M:%S")
            date_from = date_f.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f'Период отбора задан с {date_from} по {date_to}')
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
        data_for_period = transactions.loc[
            (transactions["Дата операции"] >= date_from) & (transactions["Дата операции"] <= date_to)
            ]
        logger.info(f'Период отобран с {date_from} по {date_to}')
        data_for_category = data_for_period.loc[(data_for_period['Категория'] == category)]
        logger.info(f'Сделан отбор по категории {category}')
        summ_expenses = sum(data_for_category['Сумма операции с округлением'])

    except ValueError:
        logger.error('Ошибка входных данных.')

    return data_for_category, summ_expenses
