import os
import requests
import datetime
from bs4 import BeautifulSoup


dt = datetime.datetime.today()
current_date = dt.date()


def get_html_text(link):
    r = requests.get(link, verify=False)
    return r.text


def get_rates(html):
    result = []
    soup = BeautifulSoup(html, "html.parser")
    find_div = soup.find("body").find("div", attrs={"style": 'margin-bottom: 10px;'})
    all_href = find_div.find_all("a")
    for href in all_href:
        href_name = href.get("href")
        currency_name = href_name.split("/")[-1]
        get_price = href.find("span", attrs={"class": "currency-rate-big"}).text
        get_price = get_price.replace("₸", "")
        result_string = f"Один {currency_name} равен {get_price} тенге"
        result.append(result_string)
    return result


def main():
    link = "https://ifin.kz/"
    html = get_html_text(link)
    rates = get_rates(html)
    return_rates = " ".join(rates)
    return f"{current_date}: {return_rates}"


if __name__ == "__main__":
    main()
