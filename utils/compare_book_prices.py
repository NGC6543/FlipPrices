import os
import pickle
import re

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

Каждый pickle файл это словарь где ключ это наименование, а значение
список. Список первый элемент цена, второй ссылка.
{'World of Warcraft. Перед бурей': [2939, '/catalog?prod=1261697'],
'Легенды и мифы Древней Японии': ['Цена не установлена', '/catalog?prod=1652508'],
"""
BASE_DIR = os.getcwd() + "\\Python\\Flip_prices\\"
# BASE_DIR = os.getcwd()
PATH_TO_COMPARE_PRICES = "C:\\Users\\Dimas-PC\\VScode_Projects\\Python\\Flip_prices\\utils\\compare_prices"
# PATH_TO_COMPARE_PRICES = f"{BASE_DIR}utils\\compare_prices"


def save_results(obj):
    if not os.path.exists(PATH_TO_COMPARE_PRICES):
        os.mkdir(PATH_TO_COMPARE_PRICES)
    with open(f"{PATH_TO_COMPARE_PRICES}\\compare_result.txt", "w") as f:
        for key, value in obj.items():
            f.write(
                f"Название книги: {key}, Минимальная цена {value[0]} и максимальная цены: {value[1]}"
            )
            f.write("\n")


def get_date(fname):
        r = re.compile(r"\d{4}-\d{2}-\d{2}")
        return r.findall(fname)[0]


def list_all_pages():
    compare_dict = {}
    print(os.getcwd())
    path_to_pages = f"{BASE_DIR}data_flip_pages\\"
    list_pages = os.listdir(path_to_pages)
    for page in list_pages:
        file_dict = load_pickle(f"{path_to_pages}{page}")
        # print(file_dict)
        # print("\n\n")
        for title, value in file_dict.items():
            price = value[0]
            if isinstance(price, str):
                price = 0
            get_title = compare_dict.get(title)
            if get_title:
                compared_price = compare_dict[title]
                if compared_price[0] != 0 and price <= compared_price[0]:
                    compared_price[0] = price
                if compared_price[0] != 0 and price >= compared_price[1]:
                    compared_price[1] = price
                file_date = get_date(page)
                compare_dict[title] = [compared_price[0], compared_price[1]]  # [min, max]
                continue
            compare_dict[title] = [price, price]  # [min, max]
    save_results(compare_dict)


if __name__ == "__main__":
    print("START COMPARING")
    list_all_pages()
    print("END COMPARING")



# class CompareBooks:
#     def __init__(self, pages_folder: str):
#         self.pages_folder = pages_folder
#         self.pages_path = BASE_DIR + self.pages_folder
#         self.files_in_dir = os.listdir(self.pages_path)

#     # @staticmethod
#     def first_initialization(self):
#         f_file = load_pickle(f"{self.pages_path}{self.files_in_dir[0]}")
#         for keys in f_file:
#             # # print("FFILE",f_file[keys])
#             # if f_file[keys][0] == "Цена не установлена":
#             #     f_file[keys][0] = 0
#             f_file[keys] = [f_file[keys][0], f_file[keys][0]]
#         return f_file

#     def get_min_max(self, price_list: list, sfile_price, file_date: str):
#         min_v = price_list[0]
#         max_v = price_list[1]
#         try:
#             min_date, max_date = price_list[2], price_list[3]
#         except Exception as identifier:
#             min_date, max_date = file_date, file_date
#         if isinstance(sfile_price, str):
#             return price_list[0], price_list[1], min_date, max_date
#         try:
#             if sfile_price <= price_list[0]:
#                 min_v = sfile_price
#                 min_date = file_date
#             elif sfile_price >= price_list[1]:
#                 max_v = sfile_price
#                 max_date = file_date
#         except Exception as e:
#             min_v = sfile_price
#             max_v = sfile_price
#         return min_v, max_v, min_date, max_date

#     def update(first_value, second_value, sign: str):
#         """
#         sign must be < or >
#         """
#         if second_value > first_value:
#             # second
#             return second_value

#     @staticmethod
#     def make_compare(main_file: dict, compare_file: dict, file_date: str):
#         """
#         В рамках этой функции лучше думать как о левом и правом словарях
#         main_file это левый словарь, compare_file правый
#         """
#         for keys in compare_file.keys():
#             # Возможно тут нужен будет try ... except
#             # keys может быть не во втором словаре
#             # или использовать dict.get(keys, "Цена не уст")[0]
#             # print(keys)
#             try:
#                 main_price_list = main_file[keys]
#             except Exception as e:
#                 # print(e)
#                 value_for_new_book = compare_file[keys][0]
#                 main_file[keys] = value_for_new_book, value_for_new_book
#                 main_price_list = main_file[keys]

#             second_file_price = compare_file[keys][0]
#             # Get first element of list (keys type is list and may be str or int)
#             min_v, max_v, date1, date2 = CompareBooks.get_min_max(main_price_list, second_file_price, file_date)
#             main_file[keys] = min_v, max_v, date1, date2
#         return main_file

#     def get_date(fname):
#         r = re.compile(r"\d{4}-\d{2}-\d{2}")
#         return r.findall(fname)[0]

#     def run(self):
#         main_file = CompareBooks.first_initialization(self)
#         print(f"Pages folder: {self.pages_path}")
#         for indx in range(1, len(os.listdir(self.pages_path))):
#             # print(f"RUN_{indx}")
#             fname = self.files_in_dir[indx]
#             compared_file = load_pickle(f"{self.pages_path}\\{fname}")
#             file_date = CompareBooks.get_date(fname)
#             new_file = CompareBooks.make_compare(main_file, compared_file, file_date)
#             main_file = new_file
#         main_file["Last date"] = file_date
#         self.main_file = main_file
#         print("All done")
#         # print(main_file)
#         return main_file

#     def get_current_date():
#         import datetime
#         dt = datetime.datetime.today()
#         current_date = dt.date()
#         return current_date

#     def save(self, save_pickle=False):
#         if not os.path.exists(BASE_DIR + "Compare_books"):
#             os.mkdir(BASE_DIR + "Compare_books")
#         date = CompareBooks.get_current_date()
#         save_dir = BASE_DIR + "Compare_books\\"
#         with open(f"{save_dir}\\result_file_{date}.txt", "w") as f:
#             for key, value in self.main_file.items():
#                 f.write(f"Название книги: {key}, Минимальные и максимальные цены: {value}")
#                 f.write("\n")
#         if save_pickle:
#             make_pickle(self.main_file, f"{save_dir}\\main_file_{date}.pkl")


# def just_test(folder):
#     ff = BASE_DIR + folder
#     for num, item in enumerate(os.listdir(ff)):
#         pickle_file = load_pickle(f"{ff}\\{item}")
#         list_pickle = pickle_file['Туманность Андромеды. Час Быка']
#         print(num, list_pickle)


# if __name__ == "__main__":
#     exmp = CompareBooks("data_flip_pages\\")
#     # exmp = CompareBooks("for_tests\\")
#     # just_test("for_tests\\")

#     exmp.run()
#     # exmp.save(save_pickle=True)

#     # get_date("flip 2020-05-21_35")
#     just_test("data_flip_pages\\")
