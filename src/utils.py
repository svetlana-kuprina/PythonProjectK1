from csv import excel
from typing import Any

import pandas as pd


def open_file() -> Any:
    excel_file = pd.read_excel('../data/operations.xlsx')
    return print(excel_file.head())