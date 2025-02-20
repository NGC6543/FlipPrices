import os
import sys
import re
import time
import pickle
from get_page import get_page_title
from get_offline_page import get_offline_page
from get_page_selenium import FlipBot
import secret
import get_exchange_rates


"""
Возможно стоит попробовать использовать объект DataFrame
В качестве строк использовать название книг
В качестве столбцов цену и автора
А далее использовать мультииндексы
где верхние индексы будут датой
"""

"""
TODO:
+++ 1. В функции save_pages добавить удаление всех файлов
в папке offline_pages. Чтобы эти же файлы повторно не использовались
+++ 2. Как сделать сравнение данных из файлов в том случае когда их много?
(Сохраняем в файл инфу о различии книг)
+++ 3. Может стоит дополнительно еще собирать инфу о книгах?
Быть может также указывать издательство или ссылки на эти книги?
+++ 4. Проблема в следующем: если добавяться новые книги в отложенные товары
то программа перестанет корректно сравнивать (будем сравнение разных книг)
4.1) Возможно здесь стоит использовать сдвиг (тип если книги разные, то
сделать пропустить книгу справа и рассмотреть следующую за ней)
4.2) Или заранее удалить новые добавленные книги
4.3) Или просто пропускать такие данные
4.4) Можно в фукнции difference создать переменную temp = 0
затем использовать в цикле enumerate и если слева есть книга, а справа
ее нет, то индекс temp оставить тем же, перейти на следующий цикл
и использовать этот новый индекс для правого списка
(Пробовал через цикл While, но в этом случае нужно будет делать
слишком много проверок, поэтому сделал проверку словарей)

5. Онлайн версию можно использовать для мониторинга
отдельных книг. В списке будут ссылки книг которые
не входят в список отложенных товаров.

+++ 6. В save_pages() убрать функцию с удалением всех файлов в папке
result. Возможно сделать в функции straight_path проверку наличия
файла, и если он есть то не создавать заного этот файл, т.к.
не поменяются
(В straight_path добавил проверку на существования пути (os.path.exists))

+++ 7. Может оффлейн страницы переносить в другую папку? Это для того
чтобы наши данные в data_flip_pages не создавались заново каждый раз
как я запускую скрипт.
"""


BASE_DIR = "Python\\Flip_prices\\"
# BASE_DIR = os.getcwd() + "\\"
list_titles = []
result_list = []


def get_list_all_titles():
    with open(f"{BASE_DIR}links.txt") as f:
        for i in f:
            title = get_page_title(i.rstrip())  # Function in other file
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


# From here comes the offline version
def set_dbname(date):
    "Create name depending on number of files in folder"
    number_files = os.listdir(f"{BASE_DIR}data_flip_pages")
    return f"flip {date}_{str(len(number_files) + 1)}"


def get_date_file(filename: str):
    "Extract date from filename. Example: Отложенные товары 2020-05-01.html"
    r_d = re.compile(r"\d+-\d+-\d+")
    return "".join(r_d.findall(filename))

    # Second version: Getting date from file properties
    # get_stat = os.stat(filename)
    # get_ctime = get_stat.st_ctime
    # ymd = time.strptime(time.ctime(get_ctime))
    # return f"{ymd.tm_year}-{ymd.tm_mon}-{ymd.tm_mday}"


def make_pickle(obj, path: str):
    """
    Save obj in pickle \n
    obj: object that we want save \n
    path: path to this object
    """
    dbfile = open(path, "wb")
    pickle.dump(obj, dbfile)
    dbfile.close()


def load_pickle(path: str):
    dbfile = open(path, "rb")
    db = pickle.load(dbfile)
    dbfile.close()
    return db


def clear_data_flip_folder(path_folder: str):
    "Delete all files in folder"
    # DIR = f"{BASE_DIR}{del_folder}\\"
    for item in os.listdir(path_folder):
        os.remove(BASE_DIR + item)


def move_file(from_path: str, to_path="archive_pages"):
    """
    How to move file? Copy file from old folder (from_path)
    paste file to new folder (to_path)
    delete file from old folder (from_path)
    Or use shutil.move
    """
    if not os.path.exists(f"{BASE_DIR}{to_path}"):
        os.mkdir(f"{BASE_DIR}archive_pages")
    get_last_name = from_path.split("\\")[-1]
    old_file = open(from_path, "rb").read()
    with open(f"{BASE_DIR}{to_path}\\{get_last_name}", "wb") as f:
        f.write(old_file)
    os.remove(from_path)


def save_pages():
    """
    This function generate data from offline pages
    Data saves in pickle file in data_flip_pages folder
    """
    # clear_data_flip_folder(f"{BASE_DIR}data_flip_pages")
    # if not os.path.exists(f"{BASE_DIR}offline_pages"):
    #     os.mkdir(f"{BASE_DIR}offline_pages")
    # for item in os.listdir(f"{BASE_DIR}offline_pages"):
    #     offline_page_html = f"{BASE_DIR}offline_pages\\{item}"
    #     books_title_and_price = get_offline_page(offline_page_html)
    #     date_file = get_date_file(offline_page_html)
    #     move_file(f"{BASE_DIR}offline_pages\\{item}")
    #     dbname = set_dbname(date_file)
    #     make_pickle(books_title_and_price, f"{BASE_DIR}data_flip_pages\\{dbname}")

    list_pages = os.listdir(f"{BASE_DIR}offline_pages")
    books_title_and_price = get_offline_page(list_pages)
    for item in list_pages:
        offline_page_html = f"{BASE_DIR}offline_pages\\{item}"
        move_file(f"{BASE_DIR}offline_pages\\{item}")
    date_file = get_date_file(offline_page_html)
    dbname = set_dbname(date_file)
    make_pickle(books_title_and_price, f"{BASE_DIR}data_flip_pages\\{dbname}")


def make_dict(data: list):
    "from tuple to dict (made it for test when I had tuple)"
    main_dict = {}
    for i in data:
        main_dict[i[0]] = [i[1], i[2]]
    return main_dict


def manipulate_rates(rates: str):
    if os.path.exists(f"{BASE_DIR}rates.pkl"):
        list_rate = load_pickle(f"{BASE_DIR}rates.pkl")
        last_rates = list_rate[-1]
        list_rate.append(rates)
        make_pickle(list_rate, f"{BASE_DIR}rates.pkl")
        return "".join(last_rates)
    make_pickle([rates], f"{BASE_DIR}rates.pkl")


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
    if os.path.exists(f"{BASE_DIR}result\\{fname1} and {fname2}.txt"):
        return None
    with open(f"{BASE_DIR}result\\{fname1} and {fname2}.txt", "a") as f:
        f.write(f"Compare prices {fname1} and {fname2}\n\n")
        try:
            rates = get_exchange_rates.main()
            get_last_rates = manipulate_rates(rates)
            f.write(f"Курс валют Вчера: {get_last_rates}\n")
            f.write(f"Курс валют Сегодня: {rates}\n\n")
        except Exception as e:
            print("Cant get rates from ifin.kz")
        for key, value in f_dict.items():
            try:
                value_of_second_dict = s_dict[key]
                if value[0] != value_of_second_dict[0]:
                    f.write(f"{key}, {value[0]} DIFFER FROM (Теперь цена) {key}, {value_of_second_dict[0]}\n\n")
            except Exception as e:
                pass
        f.write("Price the same")


def difference():
    files_in_dir = os.listdir(f"{BASE_DIR}data_flip_pages")
    for indx in range(len(files_in_dir) - 1):
        file1 = files_in_dir[indx]
        file2 = files_in_dir[indx + 1]
        first_file = load_pickle(f"{BASE_DIR}data_flip_pages\\{file1}")
        second_file = load_pickle(f"{BASE_DIR}data_flip_pages\\{file2}")
        straight_path(first_file, second_file, file1, file2)


def test():
    "For various purposes"
    # tt = f"{BASE_DIR}rates.pkl"
    folder = f"{BASE_DIR}data_flip_pages"
    last_file = os.listdir(folder)[-1]
    load_last_file = load_pickle(folder + f"\\{last_file}")
    # print(load_last_file)
    print(load_last_file["Жизнь пчел. Разум цветов"])


def main_offline():
    """
    This function work with offline page
    which I download manually (or using selenium)
    """
    if not os.path.exists(f"{BASE_DIR}data_flip_pages"):
        os.mkdir(f"{BASE_DIR}data_flip_pages")
    flip_page = FlipBot(secret.my_mail, secret.passw)
    flip_page.run()
    save_pages()
    difference()
    print("All done")
    # txt_fname = os.listdir(f"{BASE_DIR}result")[-1]
    # os.startfile(f"{BASE_DIR}result\\{txt_fname}")
    # test()


if __name__ == "__main__":
    # main_online()
    main_offline()
    # input("ENTER")
