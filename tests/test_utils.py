from unittest.mock import patch

import pandas as pd

from src.utils import date_filter

@patch("pandas.read_excel")
def test_date_filter(mock_df) -> None:
    """Тест функции read_excel. Используется Mock и patch"""

    read_data = pd.DataFrame(
        {
            "id": ["650703"],
            "state": ["EXECUTED"],
            "date": ["2023-09-05T11:30:32Z"],
            "amount": ["16210"],
            "currency_name": ["Sol"],
            "currency_code": ["PEN"],
            "from": ["Счет 58803664561298323391"],
            "to": ["Счет 39745660563456619397"],
            "description": ["Перевод организации"],
        }
    )
    mock_df.return_value = read_data

    expected_result = [
        {
            "id": "650703",
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": "16210",
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        }
    ]
    result = date_filter("2021-12-01 23:50:13")
    assert result == expected_result
