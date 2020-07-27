import os
import sys
import requests
import re
from bs4 import BeautifulSoup


BASE_DIR = "Python\\Flip_prices\\"
books = {}


def return_normal_prices(string):
    if string == "":
        price_book = "Цена не установлена"
        return price_book
    r = re.compile(r"\d+")
    find_int = r.findall(string)
    price_book = int("".join(find_int))
    return price_book


def get_page(filename):
    """
    In result we got "books" list, where can find Title, price and link books
    """
    soup = BeautifulSoup(open(f"{filename}", "rb"), "lxml")
    html_row = soup.find("body").find_all("div", "value", class_="row")
    for i in html_row[1:]:
        # print(i.b.text) # Тоже получает текст
        find_img_tag = i.find("img")
        title_book = find_img_tag.get("alt")  # Получение названия книги
        find_price_tag = i.find("div", class_="text_att cprice")
        price_book = return_normal_prices(find_price_tag.text)  # Получение цены
        get_a = i.a
        link_book = get_a.get("href")  # Получение ссылки на книгу
        # books.append((title_book, price_book, link_book))
        books[title_book] = [price_book, link_book]


def get_offline_page(filename):
    get_page(filename)  # Get "books" list
    # print(books)
    return books


if __name__ == "__main__":
    # filename = f"{BASE_DIR}flip_0.html"
    filename = f"{BASE_DIR}offline_pages\\Отложенные товары 2020-04-29.html"
    get_offline_page(filename)
