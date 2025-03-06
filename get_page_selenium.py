import datetime
import logging
import os
import sys

import selenium.common.exceptions as sel_exp
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


load_dotenv()


BASE_DIR = "C:\\Users\\Dimas-PC\\VScode_Projects\\Python\\Flip_prices\\"
MAIL = os.getenv('MAIL')
PASSWORD = os.getenv('PASSWORD')
SECONDS_TO_WAIT = 2


def download_page(driver, num_pages):
    """Функция для скачивания веб страниц.

    Скачивает страницы.
    """
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
    # Первая переменная позволяет запускает браузер в бэкграунде.
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
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
            driver.find_element(
                By.XPATH, f"//*[@id=\"pagination\"]/li[{li_value}]/a"
            )
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
