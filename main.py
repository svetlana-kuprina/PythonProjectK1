from src.reports import spending_by_category
from src.services import search_by_phone_numbers
from src.utils import open_file

if __name__ == "__main__":
    ex = open_file()
    dict_list = ex.to_dict(orient="records")
    print(spending_by_category(ex, 'Супермаркеты','30.12.2021'))

