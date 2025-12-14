from unittest.mock import patch, Mock

import pytest
from pandas import Timestamp

from src.utils import date_filter, kart_info, top5_transactions, currency_rates, open_file


@pytest.mark.parametrize(
    "expected_result",
    [
        [
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
    ],
)
def test_date_filter(read_data_frame, expected_result) -> None:
    """Тест функции date_filter."""

    result = date_filter("2021-12-31 23:59:59", read_data_frame)
    res = result.to_dict(orient="records")
    assert res == expected_result


def test_kart_info(read_data_frame) -> None:
    """Тест функции kart_info."""

    expected_result = [{"cashback": "", "last_digits": "7197", "total_spent": 160.89}]
    result = kart_info(read_data_frame)
    assert result == expected_result


def test_top5_transactions(read_data_frame) -> None:
    """Тест функции top5_transactions"""

    expected_result = [{"amount": 160.89, "category": "Супермаркеты", "date": "31.12.2021", "description": "Колхоз"}]
    result = top5_transactions(read_data_frame)
    assert result == expected_result


@patch("requests.get")
def test_currency_rates(mock_request_get) -> None:
    """Тест функции currency_rates запроса курса валют происходит обращение к внешнему API, используется Mock"""

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "timestamp": 1765629307,
        "base": "EUR",
        "date": "2025-12-13",
        "rates": {"RUB": 93.579038},
    }
    mock_request_get.return_value = mock_response
    open_file_user_settings = {"user_currencies": ["EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
    assert currency_rates(open_file_user_settings) == [{"currency": "EUR", "rates": 93.58}]


@patch("requests.get")
def test_currency_rates_error(mock_request_get) -> None:
    """Тест функции currency_rates запроса курса валют происходит обращение к внешнему API, используется Mock"""

    mock_response = Mock()
    # mock_response.status_code = 401
    mock_request_get.return_value = mock_response
    open_f = {}
    assert currency_rates(open_f) == []


def test_open_file_error() -> None:
    """Тест ошибок открытия файла"""

    with patch("builtins.open", side_effect=Exception) as mocked_file:
        open_file()
        assert mocked_file.called is True
        assert mocked_file.call_count == 1


@patch("requests.get")
def test_stock_price(mock_request_get) -> None:
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "Global Quote": {
            "01. symbol": "AAPL",
            "02. open": "277.9000",
            "03. high": "279.2200",
            "04. low": "276.8200",
            "05. price": "278.2800",
            "06. volume": "39532887",
            "07. latest trading day": "2025-12-12",
            "08. previous close": "278.0300",
            "09. change": "0.2500",
            "10. change percent": "0.0899%",
        }
    }
    mock_request_get.return_value = mock_response
    open_file_user_set = {"user_currencies": ["EUR"], "user_stocks": ["AAPL"]}
    assert currency_rates(open_file_user_set) == []
