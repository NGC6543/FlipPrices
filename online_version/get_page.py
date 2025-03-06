import os
import sys

import requests
from bs4 import BeautifulSoup


def get_html(link):
    r = requests.get(link)
    # print(r.text)
    return r.text


def get_title(html):
    soup = BeautifulSoup(html, "html.parser")
    find_title = soup.title.string
    # print(soup.title.string)
    # find_title = soup.find("title")
    # print(title)
    return str(find_title)


def get_page_title(link):
    html = get_html(link)
    title = get_title(html)
    return title


if __name__ == "__main__":
    link = "https://www.flip.kz/catalog?prod=1261697"
    get_page_title(link)
