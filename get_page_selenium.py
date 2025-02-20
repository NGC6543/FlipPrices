# from lib2to3.pgen2 import driver
import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
# https://stackoverflow.com/questions/16180428/can-selenium-webdriver-open-browser-windows-silently-in-the-background
# from webdriver_manager.chrome import ChromeDriverManager
import secret
import check_webdriver


"""
Notes:
find_element_by_xpath а не find_elements_by_xpath
element только один если нам не нужен список

self.driver.find_element_by_xpath('//*[@id="w_cart"]').click()
//*[@id="w_cart"] - Это можно получить если из html скопировать XPath
"""

"""
TODO:
1. Вместо time.sleep использовать специальную функцию которая ждет
пока страница не загрузится
2. Обнаружил проблему с тем что при появлении новой версии используемый
вебдрайвер перестает работать и надо скачивать новую версию вебдрайвера
Кажется для этого случая есть специальный код. Надо изучить это
"""

BASE_DIR = "Python\\Flip_prices\\"


class FlipBot:
    def __init__(self, username, passw, make_save=True):
        self.username = username
        self.password = passw
        self.make_save = make_save

    @staticmethod
    def check_webdriver():
        pass

    def download_page(self, num_pages):
        get_curr_date = datetime.datetime.now().date()
        fname_pages = f"Отложенные товары {get_curr_date}_{num_pages}.html"
        with open(f"{BASE_DIR}offline_pages\\{fname_pages}", "wb") as f:
            f.write((self.driver.page_source).encode())
        # print(f"Downlaod page: {num_pages}")

    def run(self):
        if not os.path.exists(f"{BASE_DIR}offline_pages"):
            os.mkdir(f"{BASE_DIR}offline_pages")
        try:
            # chr_options = webdriver.ChromeOptions()
            # chr_options.add_argument("user-agent=Chrome/128.0.6613.114 (Windows NT 10.0; Win64; x64")
            # self.driver = webdriver.Chrome("C:\\Program Files (x86)\\Google\\chromedriver.exe", chrome_options=chr_options)
            # self.driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver = webdriver.Chrome()
        except Exception as e:
            print(e)
            # check_webdriver.main_check_webdriver()
            print("Driver was updated")
        # finally:
        #     chrome_options = webdriver.ChromeOptions()
        #     chrome_options.add_experimental_option("disable-infobars", ['enable-automation'])
        #     self.driver = webdriver.Chrome("C:\Program Files (x86)\Google\chromedriver.exe")
        self.driver.get("https://www.flip.kz/")
        # time.sleep(2)

        # ЗДЕСЬ МЫ РЕГАЕМСЯ
        # self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div[1]/header/div[5]/div[1]/div[2]/a[1]").click()
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/header/div[3]/div[1]/a[1]").click()  # Войти
        
        # self.driver.find_element_by_xpath("//a[contains(text(), 'Войти')]")
        # self.driver.find_element_by_xpath("//input[@name=\"email\"]").send_keys(self.username)
        self.driver.find_element(By.XPATH, "//*[@id=\"auth-form\"]/div[1]/div[2]/a").click()  # Переходим на ввод пароля
        # self.driver.find_element_by_xpath("//*[@id=\"username\"]").send_keys(self.username)  # Вводим логин
        self.driver.find_element(By.XPATH, "//*[@id=\"username-pass\"]").send_keys(self.username)  # Вводим логин2
        # self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(self.password)
        # self.driver.find_element_by_xpath("//*[@id=\"password\"]").send_keys(self.password)  # Вводим пароль
        self.driver.find_element(By.XPATH, "//*[@id=\"password\"]").send_keys(self.password)  # Вводим пароль
        
        # Если будет капча попытаться допилить этот код
        # time.sleep(3)
        # self.driver.find_element_by_xpath("//*[@id=\"password\"]").send_keys(Keys.TAB + Keys.SPACE)
        # WebDriverWait(self.driver, 20).until()
        # self.driver.switch_to()
        # WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it(("//*[@id=\"recaptcha-anchor\"]/div[1]","iframe[title='reCAPTCHA']")))
        # WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(("<div class=\"recaptcha-checkbox-border\" role=\"presentation\"></div>","iframe[title='reCAPTCHA']"))).click()
        # self.driver.send_keys(Keys.TAB + Keys.TAB + Keys.TAB + " ") # Кликаем на капчу
        # self.driver.find_element_by_id("//*[@id=\"recaptcha-anchor\"]/div[1]").click() # Кликаем на капчу
        # self.driver.implicitly_wait(3)
        # time.sleep(3)

        # self.driver.find_element_by_xpath("//*[@id=\"enter_button\"]").click()  # Кликаем на войти
        self.driver.find_element(By.XPATH, "//*[@id=\"auth-form\"]/div[3]/form[1]/input[2]").click()  # Кликаем на войти
        # ЗДЕСЬ МЫ УЖЕ ВОШЛИ В АККАУНТ

        # Старая версия. Когда был список Отложенные товары
        # self.driver.find_element_by_xpath('//*[@id="w_cart"]').click()
        # self.driver.find_element_by_xpath("//*[@id='content']/div[1]/a").click()
        # time.sleep(2)  # Здесь подождать загрузки страницы
        # self.driver.get("https://www.flip.kz/user?personalis")

        # Заходим в Мой раздел
        # self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/header/div[5]/div[1]/div[2]/a[2]/span").click()
        # exel = self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/header/div[5]/div[1]/div[2]/a[2]")
        
        # Заходим в избранные
        # self.driver.find_element_by_xpath("//*[@id=\"content_left\"]/div[1]/ul/li[3]/a").click()
        # self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[3]/div/div[1]/div[1]/ul/li[3]/a").click()

        # Выше способы захода в избранное почему-то перестали работать. Также не работает наведение мышки на элемент
        # Похоже что во время работы элемент исчезает:
        # https://developer.mozilla.org/en-US/docs/Web/WebDriver/Errors/StaleElementReference
        # Ниже вариант с прямым переходом по ссылке.

        self.driver.execute_script("window.open('');")
        # Switch to the new window
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get("https://www.flip.kz/favorites")
        
        self.driver.implicitly_wait(5)
        num_pages = 1
        self.download_page(num_pages)
        if self.make_save:
            try:
                self.driver.find_element(By.XPATH, f"//*[@id=\"pagination\"]/li[2]/a").click()
                self.driver.implicitly_wait(5)
                self.download_page(num_pages+1)
                num_pages += 4
                while True:
                    # Может ли selenium читать данные со страницы?
                    # Чтобы предотвратить лишние скачивания (знаки > и >>)
                    self.driver.find_element(By.XPATH, f"//*[@id=\"pagination\"]/li[{num_pages}]/a").click()
                    self.driver.implicitly_wait(5)
                    self.download_page(num_pages)
                    num_pages += 1
            except Exception as e:
                print("All pages downloaded")


if __name__ == "__main__":
    flip_page = FlipBot(secret.my_mail, secret.passw, make_save=False)
    flip_page.run()
    # flip_page.check_webdriver
