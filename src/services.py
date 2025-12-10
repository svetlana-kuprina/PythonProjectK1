import json
import re
from typing import Dict, List

from src.utils import open_file, date_filter, kart_info


def search_by_phone_numbers(transactions: List[Dict]) -> json:


    pattern = re.compile(r'7 \d{3} \d{2}-\d{2}-\d{2}')
    list_phone_numbers = []

    for index, row in transactions:
        if re.search(pattern, row['Описание']):
            list_phone_numbers.append(row)


if __name__ == "__main__":
   ex = open_file()
   dict_l = date_filter("2021-11-01 23:50:13",ex)
   print(kart_info(dict_l))
