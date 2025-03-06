import os
import re

from get_page import get_page_title

"""
Модуль заглушка для возможного будущего развития онлайн версии.
"""

BASE_DIR = os.getcwd()
list_titles = []
result_list = []


def get_list_all_titles():
    "Function for online version"
    with open(f"{BASE_DIR}\\links.txt") as f:
        for i in f:
            title = get_page_title(i.rstrip())
            list_titles.append(title)
    # print(list_titles)


def separate_list_titles():
    "Function for online version"
    r = re.compile(r"\d+")
    for item in list_titles:
        split_items = item.split("—")[:-1]
        digit = r.findall(item)
        title_book = split_items[0].rstrip()
        price_book = int("".join(digit))
        author_book = split_items[2].rstrip()
        result_list.append((title_book, price_book, author_book))


def main_online():
    """
    This function run search on online pages
    pages taken from .txt file (see get_list_all_titles function)
    """
    get_list_all_titles()
    separate_list_titles()
    print(result_list)
