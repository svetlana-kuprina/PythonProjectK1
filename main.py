from src.reports import spending_by_category
from src.services import search_by_phone_numbers
from src.utils import open_file
from src.views import home_page

ex = open_file()

date_times = "2021-12-02 20:13:13"
print("**** вызов модуля главной страницы *****")

print(home_page(date_times))

dict_list = ex.to_dict(orient="records")

print("**** вызов модуля Поиск по телефонным номерам *****")

print(search_by_phone_numbers(dict_list))

print("**** вызов модуля Траты по категории запись в файл *****")

print(spending_by_category(ex, "Супермаркеты", "2018-01-10 00:00:00"))
