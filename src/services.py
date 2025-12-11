import json
import logging
import os
import re
from typing import Dict, List

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
log_directory = os.path.join(os.path.dirname(__file__), "../logs", "utils.log")
file_handler = logging.FileHandler(log_directory, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def search_by_phone_numbers(transactions: List[Dict]) -> json:
    """Функция поиска транзакций с телефонными номерами"""

    pattern = re.compile(r"7 \d{3}")
    list_phone_numbers = []

    for transaction in transactions:
        if re.search(pattern, transaction["Описание"]):
            list_phone_numbers.append(transaction)

    if len(list_phone_numbers) == 0:
        logger.error("Транзакции с номерами телефонов не найдены")
    else:
        logger.info("Успешно выполнен поиск по телефонам")
    return json.dumps(list_phone_numbers, ensure_ascii=False, indent=4)
