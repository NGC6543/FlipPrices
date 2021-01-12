import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

    def run(self):
        if not os.path.exists(f"{BASE_DIR}offline_pages"):
            os.mkdir(f"{BASE_DIR}offline_pages")
        try:
            self.driver = webdriver.Chrome("C:\Program Files (x86)\Google\chromedriver.exe")
        except Exception as e:
            print(e)
            check_webdriver.main_check_webdriver()
            print("Driver was updated")
        finally:
            self.driver = webdriver.Chrome("C:\Program Files (x86)\Google\chromedriver.exe")
        # self.driver = webdriver.Chrome("C:\Program Files (x86)\Google\chromedriver.exe")
        self.driver.get("https://www.flip.kz/")
        # time.sleep(2)
        # self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div[1]/header/div[5]/div[1]/div[2]/a[1]").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/header/div[5]/div[1]/div[2]/a[1]").click()
        # self.driver.find_element_by_xpath("//a[contains(text(), 'Войти')]")
        self.driver.find_element_by_xpath("//input[@name=\"email\"]").send_keys(self.username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(self.password)
        # self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div[2]/div/div/div/form/table/tbody/tr[5]/td/input")\
        #     .click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/div/div/form/table/tbody/tr[5]/td/input").click()
        self.driver.find_element_by_xpath('//*[@id="w_cart"]').click()
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/a").click()
        time.sleep(2) # Здесь подождать загрузки страницы
        get_curr_date = datetime.datetime.now().date()
        fname_pages = f"Отложенные товары {get_curr_date}.html"
        if self.make_save:
            with open(f"{BASE_DIR}offline_pages\\{fname_pages}", "wb") as f:
                f.write((self.driver.page_source).encode())


if __name__ == "__main__":
    flip_page = FlipBot(secret.my_mail, secret.passw, make_save=False)
    flip_page.run()
    # flip_page.check_webdriver
