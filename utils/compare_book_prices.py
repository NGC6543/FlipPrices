import os
import re
from pathlib import Path

from load_make_pickle import load_pickle


"""
Создать модуль который будет находить минимальную и максимальную
цену книги. Одновременно с этим отображать дату, когда эти цены
были.
Можно попробовать инициализировать в переменную первые значения из первого
файла. И далее сравнивать новые значения из следующих файлов с этой
переменной (думаю переменная будет dict)


Или еще можно сделать функцию, которая по названию книги
ищет ее максимальную и минимальную цены, и какого числа они были
(можно добавить также среднеарифметическое и курс валюты)
Сделать это примерно так: просматриваем все файлы в папке
data_flip_pages. Открываем первый и второй
Сравниваем цены одних и тех же книг и создаем переменные минимума
и максимума с минимумом и максимумом цены.
Думаю хранить это в отдельном pickle файле
"""

"""
TODO:
Имеется старая версия. Необходимо сделать другой способ сравнения
в соотвествии с целью определенной выше.

+++ 1. Мне кажется не верно сравниваются значения.
В результате оказывается, что и мин и макс значения равны 0.
+++ 2. Добавить дату когда была минимальная и максимальная цена.

Каждый pickle файл это словарь где ключ это наименование, а значение
список. Список первый элемент цена, второй ссылка.
{'World of Warcraft. Перед бурей': [2939, '/catalog?prod=1261697'],
'Легенды и мифы Древней Японии': ['Цена не установлена', '/catalog?prod=1652508'],
"""


BASE_DIR = Path(__file__).resolve().parent.parent
PATH_TO_COMPARE_PRICES = f"{BASE_DIR}\\utils\\compare_prices"


def save_results(obj):
    if not os.path.exists(PATH_TO_COMPARE_PRICES):
        os.mkdir(PATH_TO_COMPARE_PRICES)
    with open(f"{PATH_TO_COMPARE_PRICES}\\compare_result.txt", "w") as f:
        for key, value in obj.items():
            f.write(
                f"Название книги: {key}, Минимальная цена {value['min_price']} {value['min_date']} "
                f"Максимальная цена: {value['max_price']} {value['max_date']}"
            )
            f.write("\n")


def get_date(fname):
    r = re.compile(r"\d{4}-\d{2}-\d{2}")
    return r.findall(fname)[0]


def list_all_pages():
    compare_dict = {}
    print(os.getcwd())
    path_to_pages = f"{BASE_DIR}\\data_flip_pages\\"
    list_pages = os.listdir(path_to_pages)
    for page in list_pages:
        load_pickle_to_dict = load_pickle(f"{path_to_pages}{page}")
        for title, value in load_pickle_to_dict.items():
            price = value[0]
            if isinstance(price, str):
                continue
            get_title = compare_dict.get(title)
            file_date = get_date(page)
            if not get_title:
                compare_dict[title] = {'min_price': price,
                                       'max_price': price,
                                       'min_date': file_date,
                                       'max_date': file_date}
            else:
                compared_price = compare_dict[title]
                # Сначала вычисляем минимум
                if price <= compared_price['min_price']:
                    compared_price['min_price'] = price
                    compared_price['min_date'] = file_date
                if price >= compared_price['max_price']:
                    compared_price['max_price'] = price
                    compared_price['max_date'] = file_date
                compare_dict[title] = compared_price
    save_results(compare_dict)


if __name__ == "__main__":
    print("START COMPARING")
    list_all_pages()
    print("END COMPARING")
