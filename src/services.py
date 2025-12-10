import re

from pandas import DataFrame


def search_by_phone_numbers(date_fl: DataFrame):
    pattern = re.compile(r'+7\s\d{3}\s\d{2}')

