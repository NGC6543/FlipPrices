import os
import re
from pathlib import Path

import requests

import get_exchange_rates
import get_page_selenium
from get_offline_page import get_offline_page
from utils.load_make_pickle import load_pickle, make_pickle

"""
TODO:
1. Вместо путей попробовать использовать Pathlib. В частности:
https://docs.python.org/3/library/pathlib.html#pathlib.Path.resolve
"""


BASE_DIR = Path(__file__).resolve().parent


def set_dbname(date):
    "Create name depending on number of files in folder"
    number_files = os.listdir(f"{BASE_DIR}\\data_flip_pages")
    return f"flip {date}_{str(len(number_files) + 1)}"


def get_date_file(filename: str):
    "Extract date from filename. Example: Отложенные товары 2020-05-01.html"
    r_d = re.compile(r"\d+-\d+-\d+")
    return "".join(r_d.findall(filename))


def clear_data_flip_folder(path_folder: str):
    """Delete all files in folder."""
    for item in os.listdir(path_folder):
        os.remove(BASE_DIR + "\\" + item)


def move_file(from_path: str, to_path="archive_pages"):
    """
    How to move file? Copy file from old folder (from_path)
    paste file to new folder (to_path)
    delete file from old folder (from_path)
    Or use shutil.move
    """
    if not os.path.exists(f"{BASE_DIR}\\{to_path}"):
        os.mkdir(f"{BASE_DIR}\\archive_pages")
    get_last_name = from_path.split("\\")[-1]
    old_file = open(from_path, "rb").read()
    with open(f"{BASE_DIR}\\{to_path}\\{get_last_name}", "wb") as f:
        f.write(old_file)
    os.remove(from_path)


def save_pages():
    """
    This function generate data from offline pages
    Data saves in pickle file in data_flip_pages folder
    """
    list_pages = os.listdir(f"{BASE_DIR}\\offline_pages")
    books_title_and_price = get_offline_page(list_pages)
    for item in list_pages:
        offline_page_html = f"{BASE_DIR}\\offline_pages\\{item}"
        move_file(f"{BASE_DIR}\\offline_pages\\{item}")
    date_file = get_date_file(offline_page_html)  # type: ignore
    dbname = set_dbname(date_file)
    make_pickle(
        books_title_and_price, f"{BASE_DIR}\\data_flip_pages\\{dbname}"
    )


def make_dict(data: list):
    "from tuple to dict (made it for test when a had tuple)"
    main_dict = {}
    for i in data:
        main_dict[i[0]] = [i[1], i[2]]
    return main_dict


def manipulate_rates(rates: str):
    if os.path.exists(f"{BASE_DIR}\\rates.pkl"):
        list_rate = load_pickle(f"{BASE_DIR}\\rates.pkl")
        last_rates = list_rate[-1]
        list_rate.append(rates)
        make_pickle(list_rate, f"{BASE_DIR}\\rates.pkl")
        return "".join(last_rates)
    make_pickle([rates], f"{BASE_DIR}\\rates.pkl")


def straight_path(f_dict: dict, s_dict: dict, fname1: str, fname2: str):
    """
    Эта фукция как бы прямой путь. У нас есть как бы два списка книги слева
    и книги справа. Каждый элемент слева сравнивается с каждым справа
    Но делается это с помощью словаря.
    Книги справа новее, поэтому там могут быть новые элементы или некоторые
    элементы которые есть слева, могут не быть справа
    (то есть я купил или удалил эту книгу)
    Поэтому чтобы избежать множественных проверок списка я пытаюсь с помощью
    словаря найти ключ(название книги) слева в словаре справа по этому же ключу
    если ключа нет то и книги справа такой нет, а значит просто пропускаем это
    если ключ есть то берем значение этого ключа и сравниваем цены
    Структура словаря такая: ключ: значение, у меня это так:
    Название книги (str): [цена (int), ссылка на эту книгу (str)]
    """
    if not os.path.exists(f"{BASE_DIR}\\result\\"):
        os.mkdir(f"{BASE_DIR}\\result\\")
    if os.path.exists(f"{BASE_DIR}\\result\\{fname1} and {fname2}.txt"):
        return None
    with open(
        f"{BASE_DIR}\\result\\{fname1} and {fname2}.txt", "a+", encoding="UTF-8"
    ) as f:
        f.write(f"Compare prices {fname1} and {fname2}\n\n")
        try:
            rates = get_exchange_rates.main()
            get_last_rates = manipulate_rates(rates)
            f.write(f"Курс валют Вчера: {get_last_rates}\n")
            f.write(f"Курс валют Сегодня: {rates}\n\n")
        except requests.exceptions.ConnectionError:
            print("Cant get rates from ifin.kz")
        for key, value in f_dict.items():
            value_of_second_dict = s_dict.get(key)
            if value_of_second_dict is not None and value[0] != value_of_second_dict[0]:
                f.write(
                    f"{key}, {value[0]} DIFFER FROM {key},"
                    f" {value_of_second_dict[0]} (Теперь цена) \n\n"
                )
        f.write("Price the same")


def difference():
    files_in_dir = os.listdir(f"{BASE_DIR}\\data_flip_pages")
    files_in_dir.sort()
    if len(files_in_dir) < 2:
        file1 = files_in_dir[-1]
        file2 = files_in_dir[-1]
    else:
        file1 = files_in_dir[-2]
        file2 = files_in_dir[-1]
    print("Сравниваемые файлы: ", file1, file2)
    first_file = load_pickle(f"{BASE_DIR}\\data_flip_pages\\{file1}")
    second_file = load_pickle(f"{BASE_DIR}\\data_flip_pages\\{file2}")
    straight_path(first_file, second_file, file1, file2)


def test():
    "For various purposes"
    # tt = f"{BASE_DIR}rates.pkl"
    folder = f"{BASE_DIR}\\data_flip_pages"
    last_file = "flip 2025-02-26_547"
    # last_file = os.listdir(folder)[-1]
    print(last_file)
    load_last_file = load_pickle(folder + f"\\{last_file}")
    print(load_last_file)
    print(load_last_file["Жизнь пчел. Разум цветов"])


def main_offline():
    """
    This function work with offline page
    which I download manually (or using selenium)
    """
    if not os.path.exists(f"{BASE_DIR}\\data_flip_pages"):
        os.mkdir(f"{BASE_DIR}\\data_flip_pages")
    get_page_selenium.main()
    save_pages()
    difference()
    print("All done")


if __name__ == "__main__":
    main_offline()
    # test()
