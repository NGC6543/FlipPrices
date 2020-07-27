import os
import requests
from bs4 import BeautifulSoup
import zipfile


"""
1. Мы скачали зип архив теперь его надо разархивировать
и удалить сам архив +++
Осталось решить проблему с доступом файла к диску С,
то есть решить проблему с разрешением (mode)

2. Также нужно дописать второй способ скачивания

Первый способ основывается на построении скачивающей ссылки
то есть в заготовленную ссылку вставляется номер версии и таким
образом происходит скачивание этой версии
https://chromedriver.storage.googleapis.com/{ЗДЕСЬ НОМЕР ВЕРСИИ}/chromedriver_win32.zip

Последнюю версию можно получить по ссылке:
https://chromedriver.storage.googleapis.com/LATEST_RELEASE

Второй способ более традиционный: заходим на сайт ищем определенные
теги, кликаем на ссылки по этим тегам, заходим туда, ищем другие теги
и так далее, пока не доберемся до искомой ссылки.
Этот метод надежней т.к., в этом случае мы можем не беспокоиться
если построение ссылки изменится
"""


# BASE_DIR = "Python\\TEST\\"
download_path = "C:\\Program Files (x86)\\Google\\"


def get_html(url: str, download_file=False):
    if not download_file:
        r = requests.get(url)
        return r.text
    r = requests.get(url, stream=True)
    filename = "test" + ".zip"
    full_path = f"{download_path}{filename}"
    with open(full_path, 'bw') as f:
        for chunk in r.iter_content(4096):
            f.write(chunk)
    main_zip = zipfile.ZipFile(full_path)
    main_zip.extract("chromedriver.exe", path=download_path)
    main_zip.close()
    os.remove(full_path)

# def html_test(url: str):
#     r = requests.get(url, stream=True)
#     filename = "test" + ".zip"
#     full_path = f"{download_path}{filename}"
#     with open(full_path, 'bw') as f:
#         for chunk in r.iter_content(4096):
#             f.write(chunk)
    # return r.text


def get_download_link(html, last_version: str):
    soup = BeautifulSoup(html, "html.parser")
    get_a_tag = soup.find("tbody").find_all("a")
    # print(get_a_tag)
    for item in get_a_tag:
        cur_version = item.get_text()
        if last_version in cur_version:
            return item.get("href")


def get_test(html, last_version: str):
    soup = BeautifulSoup(html, "html.parser")
    get_a_tag = soup.find("tbody").find_all("a")
    print(get_a_tag)
    # for item in get_a_tag:
    #     print(item)
        # cur_version = item.get_text()
        # if last_version in cur_version:
        #     return item.get("href")


def main_check_webdriver():
    link = "https://chromedriver.chromium.org/downloads"
    last_version = get_html("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
    # First version
    html_download_link = get_html(f"https://chromedriver.storage.googleapis.com/{last_version}/chromedriver_win32.zip", True)

    # Second version
    # html = get_html(link)
    # download_link = get_download_link(html, last_version)

    # html_download_link = html_test(download_link)
    # tt = get_test(html_download_link, last_version)
    # print(html_download_link)


if __name__ == "__main__":
    main_check_webdriver()
