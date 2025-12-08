import json
from unittest.mock import patch, Mock

from src.views import home_page

@patch("currency_r, stock_price_result")
def test_home_page(mock_currency_r, mock_stock_price_result):

    mock_currency = [{"currency": "USD", "rates": 76.69}, {"currency": "EUR", "rates": 89.45}]
    mock_currency_r.return_value = mock_currency
    mock_stock_price_r = [{"stock": "AAPL", "rates": "280.5400"},
            {"stock": "AMZN", "rates": "230.3200"},
            {"stock": "GOOGL", "rates": "319.4900"},
            {"stock": "MSFT", "rates": "482.5150"},
            {"stock": "TSLA", "rates": "453.0300"}]
    mock_stock_price_result.return_value = mock_stock_price_r

    data = {"greetings": "Добрый вечер", "cards":[{"last_digits": "7197", "total_spent": 99.0, "cashback": "---"},
            {"last_digits": "7197", "total_spent": 199.0, "cashback": "---"},
            {"last_digits": "7197", "total_spent": 99.22, "cashback": "---"},
            {"last_digits": "5091", "total_spent": 1.07, "cashback": "---"},
            {"last_digits": "7197", "total_spent": 15.0, "cashback": "---"},
            {"last_digits": "7197", "total_spent": 496.51, "cashback": "---"},
            {"last_digits": "5091", "total_spent": 5510.8, "cashback": "---"}],
            "top_transactions":
            [{"date": "02.12.2021", "amount": 5510.8, "category": "Каршеринг", "description": "Ситидрайв"},
            {"date": "02.12.2021", "amount": 496.51, "category": "Супермаркеты", "description": "Магнит"},
            {"date": "01.12.2021", "amount": 199.0, "category": "Дом и ремонт", "description": "Строитель"},
            {"date": "01.12.2021", "amount": 99.22, "category": "Супермаркеты", "description": "Дикси"},
            {"date": "01.12.2021", "amount": 99.0, "category": "Фастфуд", "description": "IP Yakubovskaya M.V."}],
            "currency_rates":
            [{"currency": "USD", "rates": 76.69}, {"currency": "EUR", "rates": 89.45}],
            "stock_price":
            [{"stock": "AAPL", "rates": "280.5400"},
            {"stock": "AMZN", "rates": "230.3200"},
            {"stock": "GOOGL", "rates": "319.4900"},
            {"stock": "MSFT", "rates": "482.5150"},
            {"stock": "TSLA", "rates": "453.0300"}]}

    exp = home_page("2021-12-02 20:13:13")
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    assert exp == json_data