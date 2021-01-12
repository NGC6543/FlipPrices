import os
import pickle
import re
from main_flip_prices import load_pickle
from main_flip_prices import make_pickle


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
1. Добавить дату когда были минимальные и максимальные значения
+- 2. Использовать main_file.pkl как отправную точку.
То есть вместо того чтобы заново анализировать все файлы
мы начнем анализ с main_file.pkl который содержит результаты
всех прошлых файлов. Соответственно нужно как сказать ему какой файл
был последним.
(Сделал ключ Last date в главном словаре main_file)
3. Разобраться с функцией get_min_max
Работает некорректно (вроде корректно работает, нужны еще тесты)
4. Обнаружил проблему что если в следующем файле pickle появяться
новые книги, то эти книги вообще не будут учитываться.
Нужно сделать так что, если они новые то просто добавлялись
без сравнений
"""

BASE_DIR = "Python\\Flip_prices\\"
# BASE_DIR = os.getcwd()


class CompareBooks:
    def __init__(self, pages_folder: str):
        self.pages_folder = pages_folder
        self.pages_path = BASE_DIR + self.pages_folder
        self.files_in_dir = os.listdir(self.pages_path)

    # @staticmethod
    def first_initialization(self):
        f_file = load_pickle(f"{self.pages_path}{self.files_in_dir[0]}")
        for keys in f_file:
            f_file[keys] = [f_file[keys][0], f_file[keys][0]]
        return f_file

    def get_min_max(price_list: list, sfile_price, file_date: str):
        """
        sfile_price может быть как int так и str
        """
        try:
            min_date, max_date = price_list[2], price_list[3]
        except Exception as identifier:
            min_date, max_date = "No Date", "No Date"
        min_v, max_v = price_list[0], price_list[1]
        if isinstance(sfile_price, str):
            return price_list[0], price_list[1], None, None
            # return *price_list
        # Check min price
        if isinstance(price_list[0], int) and sfile_price <= price_list[0]:
            # min_v = (sfile_price, file_date)
            min_v = sfile_price
            min_date = file_date
        # Check max price
        if isinstance(price_list[1], int) and sfile_price >= price_list[1]:
            # max_v = (sfile_price, file_date)
            max_v = sfile_price
            max_date = file_date
        return min_v, max_v, min_date, max_date
        # return min_v, max_v, [f"MIN_Date: {min_date}", f"MAX_Date: {max_date}"]

    @staticmethod
    def make_compare(main_file: dict, compare_file: dict, file_date: str):
        """
        В рамках этой функции лучше думать как о левом и правом словарях
        main_file это левый словарь, compare_file правый
        """
        for keys in compare_file.keys():
            # Возможно тут нужен будет try ... except
            # keys может быть не во втором словаре
            # или использовать dict.get(keys, "Цена не уст")[0]

            # main_price_list = main_file[keys]  # Здесь list(min and max value)
            # second_file_price = compare_file.get(keys, "Цена")[0]
            # min_v, max_v = CompareBooks.get_min_max(main_price_list, second_file_price, file_date)
            # main_file[keys] = min_v, max_v
            try:
                main_price_list = main_file[keys]
                second_file_price = compare_file.get(keys, "Цена")[0]
                # Get first element of list (keys type is list and may be str or int)
                # second_file_price = compare_file[keys][0]
                min_v, max_v, date1, date2 = CompareBooks.get_min_max(main_price_list, second_file_price, file_date)
                if date1 is not None:
                    main_file[keys] = min_v, max_v, date1, date2
                else:
                    main_file[keys] = min_v, max_v
            except Exception as e:
                pr = compare_file[keys][0]
                main_file[keys] = [pr, pr]
        return main_file

    def get_date(fname):
        r = re.compile(r"\d{4}-\d{2}-\d{2}")
        return r.findall(fname)[0]

    def run(self):
        main_file = CompareBooks.first_initialization(self)
        print(f"Pages folder: {self.pages_path}")
        for indx in range(1, len(os.listdir(self.pages_path))):
            fname = self.files_in_dir[indx]
            compared_file = load_pickle(f"{self.pages_path}\\{fname}")
            file_date = CompareBooks.get_date(fname)
            new_file = CompareBooks.make_compare(main_file, compared_file, file_date)
            main_file = new_file
        main_file["Last date"] = file_date
        self.main_file = main_file
        print("All done")
        # print(main_file)
        return main_file

    def get_current_date():
        import datetime
        dt = datetime.datetime.today()
        current_date = dt.date()
        return current_date

    def save(self, save_pickle=False):
        if not os.path.exists(BASE_DIR + "Compare_books"):
            os.mkdir(BASE_DIR + "Compare_books")
        date = CompareBooks.get_current_date()
        save_dir = BASE_DIR + "Compare_books\\"
        with open(f"{save_dir}\\result_file_{date}.txt", "w") as f:
            for key, value in self.main_file.items():
                f.write(f"Название книги: {key}, Минимальные и максимальные цены: {value}")
                f.write("\n")
        if save_pickle:
            make_pickle(self.main_file, f"{save_dir}\\main_file_{date}.pkl")


def just_test(folder):
    ff = BASE_DIR + folder
    for num, item in enumerate(os.listdir(ff)):
        pickle_file = load_pickle(f"{ff}\\{item}")
        print(num, pickle_file['Жизнь пчел. Разум цветов'])


if __name__ == "__main__":
    exmp = CompareBooks("data_flip_pages\\")
    # exmp = CompareBooks("for_tests\\")

    exmp.run()
    exmp.save(save_pickle=False)

    # get_date("flip 2020-05-21_35")
    # just_test("data_flip_pages\\")
