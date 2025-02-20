import requests


"""
Trying get page using POST method. Alternative for selenium
"""

BASE_DIR = "Python\\Flip_prices\\"


def main_get_post():
    web_page = "https://www.flip.kz/"
    req_test = requests.request("POST", web_page)
    r_text = req_test.text
    with open(f"{BASE_DIR}r_test.html", "w+") as f:
        f.write(r_text)
    # print(req_test.text)
    print(dir(req_test))


if __name__ == "__main__":
    main_get_post()