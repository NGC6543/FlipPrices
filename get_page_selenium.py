import datetime
import logging
import os
import sys
import time

import selenium.common.exceptions as sel_exp
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv


# https://stackoverflow.com/questions/16180428/can-selenium-webdriver-open-browser-windows-silently-in-the-background


load_dotenv()


BASE_DIR = "C:\\Users\\Dimas-PC\\VScode_Projects\\Python\\Flip_prices\\"
DRIVER_PATH = "C:\\Program Files (x86)\\Google\\chromedriver.exe"
MAIL = os.getenv('MAIL')
PASSWORD = os.getenv('PASSWORD')
SECONDS_TO_WAIT = 2


def download_page(driver, num_pages):
    get_curr_date = datetime.datetime.now().date()
    fname_pages = f"Отложенные товары {get_curr_date}_{num_pages}.html"
    with open(f"{BASE_DIR}offline_pages\\{fname_pages}", "wb") as f:
        f.write((driver.page_source).encode())
    print(f"Downloaded page: {num_pages}")


def get_page(url):
    """Функция для входа в аккаунт.

    После входа заходим на страницу избранного.
    """
    print(os.getcwd())
    if not os.path.exists("offline_pages"):
        os.mkdir("offline_pages")
        logging.info('Папка offline_pages создана.')

    # Настраиваем драйвер.
    driver = webdriver.Firefox()
    driver.implicitly_wait(SECONDS_TO_WAIT)

    # Начинаем входить в аккаунт.
    driver.get(url)
    # Войти в аккаунт.
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div[1]/div/header/div[3]/div[1]/a[1]"
    ).click()
    try:
        driver.find_element(By.XPATH, "//*[@id=\"username\"]")
    except sel_exp.NoSuchElementException:
        logging.warning("Поля для ввода логина нет.")
        # Войти с помощью пароля.
        driver.find_element(
            By.XPATH, "//*[@id=\"auth-form\"]/div[1]/div[2]/a"
        ).click()

    # Вводим логин.
    driver.find_element(
        By.XPATH, "//*[@id=\"username-pass\"]"
    ).send_keys(MAIL)  # type: ignore
    # Вводим пароль.
    driver.find_element(
        By.XPATH, "//*[@id=\"password\"]"
    ).send_keys(PASSWORD)  # type: ignore
    # Кликаем на войти.
    driver.find_element(
        By.XPATH, "//*[@id=\"auth-form\"]/div[3]/form[1]/input[2]"
    ).click()  
    # ЗДЕСЬ МЫ УЖЕ ВОШЛИ В АККАУНТ.

    # Заходим в избранное.
    driver.find_element(By.XPATH, "//*[@id=\"w_cart\"]").click()

    num_page = 1
    li_value = 7
    while True:
        try:
            driver.find_element(By.XPATH, f"//*[@id=\"pagination\"]/li[{li_value}]/a")
        except sel_exp.NoSuchElementException:
            logging.debug("Или первая или последняя страница.")
            download_page(driver, num_page)
            break
        download_page(driver, num_page)
        num_page += 1
        driver.find_element(
            By.XPATH, f"//*[@id=\"pagination\"]/li[{li_value}]/a"
        ).click()
        li_value = 9

    driver.close()


# //*[@id="pagination"]/li[7]/a
# //*[@id="pagination"]/li[9]/a
# //*[@id="pagination"]/li[9]/a
# //*[@id="pagination"]/li[9]/a


# //*[@id="pagination"]/li[1]/a
# //*[@id="pagination"]/li[2]/a

def main():
    """Главная функция.

    Управляет событиями.
    """
    url = "https://www.flip.kz/"
    get_page(url)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARNING,
        handlers=[logging.StreamHandler(sys.stdout),
                  logging.FileHandler('main.log')
                  ],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    main()





# class FlipBot:
#     def __init__(self, username, passw, make_save=True):
#         self.username = username
#         self.password = passw
#         self.make_save = make_save

#     @staticmethod
#     def check_webdriver():
#         pass

#     def download_page(self, num_pages):
#         get_curr_date = datetime.datetime.now().date()
#         fname_pages = f"Отложенные товары {get_curr_date}_{num_pages}.html"
#         with open(f"{BASE_DIR}offline_pages\\{fname_pages}", "wb") as f:
#             f.write((self.driver.page_source).encode())
#         print(f"Downlaod page: {num_pages}")

#     def run(self):
#         if not os.path.exists(f"{BASE_DIR}offline_pages"):
#             os.mkdir(f"{BASE_DIR}offline_pages")
#         try:
#             self.driver = webdriver.Chrome("C:\Program Files (x86)\Google\chromedriver.exe")
#         except Exception as e:
#             print(e)
#             check_webdriver.main_check_webdriver()
#             print("Driver was updated")
#         finally:
#             self.driver = webdriver.Chrome("C:\Program Files (x86)\Google\chromedriver.exe")
#         self.driver.get("https://www.flip.kz/")
#         # time.sleep(2)

#         # ЗДЕСЬ МЫ РЕГАЕМСЯ
#         # self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div[1]/header/div[5]/div[1]/div[2]/a[1]").click()
#         self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/header/div[5]/div[1]/div[2]/a[1]").click()  # Войти
#         # self.driver.find_element_by_xpath("//a[contains(text(), 'Войти')]")
#         # self.driver.find_element_by_xpath("//input[@name=\"email\"]").send_keys(self.username)
#         self.driver.find_element_by_xpath("//*[@id=\"username\"]").send_keys(self.username)  # Вводим логин
#         # self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(self.password)
#         self.driver.find_element_by_xpath("//*[@id=\"password\"]").send_keys(self.password)  # Вводим пароль
#         # self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div[2]/div/div/div/form/table/tbody/tr[5]/td/input")\
#         #     .click()
#         self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]/form/input[1]").click()  # Кликаем на войти
#         # ЗДЕСЬ МЫ УЖЕ ВОШЛИ В АККАУНТ

#         # Старая версия. Когда был список Отложенные товары
#         # self.driver.find_element_by_xpath('//*[@id="w_cart"]').click()
#         # self.driver.find_element_by_xpath("//*[@id='content']/div[1]/a").click()
#         # time.sleep(2)  # Здесь подождать загрузки страницы

#         # Заходим в Мой раздел
#         self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/header/div[5]/div[1]/div[2]/a[2]/span").click()
#         # Заходим в избранные
#         self.driver.find_element_by_xpath("//*[@id=\"content_left\"]/div[1]/ul/li[3]/a").click()
#         self.driver.implicitly_wait(5)
#         num_pages = 1
#         self.download_page(num_pages)
#         if self.make_save:
#             try:
#                 self.driver.find_element_by_xpath(f"//*[@id=\"pagination\"]/li[2]/a").click()
#                 self.driver.implicitly_wait(5)
#                 self.download_page(num_pages+1)
#                 num_pages += 4
#                 while True:
#                     # Может ли selenium читать данные со страницы?
#                     # Чтобы предотвратить лишние скачивания (знаки > и >>)
#                     self.driver.find_element_by_xpath(f"//*[@id=\"pagination\"]/li[{num_pages}]/a").click()
#                     self.driver.implicitly_wait(5)
#                     self.download_page(num_pages)
#                     num_pages += 1
#             except Exception as e:
#                 print("All pages downloaded")


# if __name__ == "__main__":
#     flip_page = FlipBot(MAIL, PASSWORD, make_save=True)
#     flip_page.run()
#     # flip_page.check_webdriver
