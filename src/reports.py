import datetime
from typing import Optional

import pandas as pd


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция формирования отчета, возвращает траты по заданной категории за последние три месяца"""
    if date is None:
        date = datetime.date.today()
        new_time_obj = date - datetime.timedelta(days=90)
        date_to = date.strftime("%d-%m-%Y")
        date_from = new_time_obj.strftime("%d-%m-%Y")
    else:
        date_to = datetime.datetime.strptime(date, "%d-%m-%Y")
        date_from = date_to- datetime.timedelta(days=90)
        # date_to = date.strftime("%d-%m-%Y")
        # date_from = new_time_obj.strftime("%d-%m-%Y")

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    data_for_period = transactions.loc[
            (transactions["Дата операции"] >= date_from) & (transactions["Дата операции"] <= date_to)
            ]

    return date_from, date_to, data_for_period
