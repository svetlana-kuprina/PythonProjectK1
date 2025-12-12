from unittest.mock import patch, Mock

import pandas as pd
from pandas import Timestamp

from src.utils import date_filter, kart_info, top5_transactions, currency_rates


def test_date_filter() -> None:
    """Тест функции date_filter."""

    read_data = pd.DataFrame(
        {
            "Дата операции": ["31.12.2021 16:44:00"],
            "Дата платежа": ["31.12.2021"],
            "Номер карты": ["*7197"],
            "Статус": ["OK"],
            "Сумма операции": [-160.89],
            "Валюта операции": ["RUB"],
            "Сумма платежа": [-160.89],
            "Валюта платежа": ["RUB"],
            "Кэшбэк": [""],
            "Категория": ["Супермаркеты"],
            "MCC": ["5411"],
            "Описание": ["Колхоз"],
            "Бонусы (включая кэшбэк)": [""],
            "Округление на инвесткопилку": [0.00],
            "Сумма операции с округлением": [160.89],
        }
    )

    expected_result = [
        {
            "MCC": "5411",
            "Бонусы (включая кэшбэк)": "",
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Дата операции": Timestamp("2021-12-31 16:44:00"),
            "Дата платежа": "31.12.2021",
            "Категория": "Супермаркеты",
            "Кэшбэк": "",
            "Номер карты": "*7197",
            "Округление на инвесткопилку": 0.0,
            "Описание": "Колхоз",
            "Статус": "OK",
            "Сумма операции": -160.89,
            "Сумма операции с округлением": 160.89,
            "Сумма платежа": -160.89,
        }
    ]
    result = date_filter("2021-12-31 23:59:59", read_data)
    res = result.to_dict(orient="records")
    assert res == expected_result


def test_kart_info() -> None:
    """Тест функции kart_info."""

    read_d = pd.DataFrame(
        {
            "Дата операции": ["31.12.2021 16:44:00"],
            "Дата платежа": ["31.12.2021"],
            "Номер карты": ["*7197"],
            "Статус": ["OK"],
            "Сумма операции": [-160.89],
            "Валюта операции": ["RUB"],
            "Сумма платежа": [-160.89],
            "Валюта платежа": ["RUB"],
            "Кэшбэк": [""],
            "Категория": ["Супермаркеты"],
            "MCC": ["5411"],
            "Описание": ["Колхоз"],
            "Бонусы (включая кэшбэк)": [""],
            "Округление на инвесткопилку": [0.00],
            "Сумма операции с округлением": [160.89],
        }
    )

    expected_result = [{"cashback": "", "last_digits": "7197", "total_spent": 160.89}]
    result = kart_info(read_d)
    assert result == expected_result


def test_top5_transactions() -> None:
    read_d = pd.DataFrame(
        {
            "Дата операции": ["31.12.2021 16:44:00"],
            "Дата платежа": ["31.12.2021"],
            "Номер карты": ["*7197"],
            "Статус": ["OK"],
            "Сумма операции": [-160.89],
            "Валюта операции": ["RUB"],
            "Сумма платежа": [-160.89],
            "Валюта платежа": ["RUB"],
            "Кэшбэк": [""],
            "Категория": ["Супермаркеты"],
            "MCC": ["5411"],
            "Описание": ["Колхоз"],
            "Бонусы (включая кэшбэк)": [""],
            "Округление на инвесткопилку": [0.00],
            "Сумма операции с округлением": [160.89],
        }
    )

    expected_result = [{"amount": 160.89, "category": "Супермаркеты", "date": "31.12.2021", "description": "Колхоз"}]
    result = top5_transactions(read_d)
    assert result == expected_result


# @patch("requests.get")
# def test_currency_rates(mock_request_get) -> None:
#     """Тест функции currency_rates запроса курса валют происходит обращение к внешнему API, используется Mock"""
#
#     mock_response = Mock()
#     mock_response.status_code = 200
#     mock_response.text = {
#         "success": True,
#         "timestamp": 1765191787,
#         "base": "EUR",
#         "date": "2025-12-08",
#         "rates": {"RUB": 89.4500},
#     }
#     mock_request_get.return_value = mock_response
#
#     assert currency_rates() == [{"currency": "EUR", "rates": 89.45}]
#     mock_request_get.assert_called_with(
#         "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=EUR",
#         headers={"apikey": "Hzn1ZfOBV2bvKNQBCgsZW72APuJSZI72"},
#         data={},
#     )
