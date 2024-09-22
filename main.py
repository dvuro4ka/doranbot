import requests

from lxml import html, etree
from test import main as get_timezone
from bs4 import BeautifulSoup
from collect_img import get_img


def send_request(session, url, params=None, headers=None, proxies=None, timeout=30, method='POST'):
    try:
        response = session.post(url, data=params, headers=headers, proxies=proxies, timeout=timeout)

        if response.status_code == 200:
            print("Request to {} succeeded".format(url))
            return response.text
        else:
            print(f"Request to {url} failed with status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def parse_html_with_xpath(html, xpath):
    soup = BeautifulSoup(html, 'html.parser')
    dom = etree.HTML(str(soup))
    elements = dom.xpath(xpath)
    if elements:
        return elements[0]
    else:
        print("No block found with XPath {}".format(xpath))
        return None


def handle(params):
    data = params
    name = data["name"].split(" ")[0]
    if (data["date"].split('.')[0] and data["date"].split('.')[1] and data["date"].split('.')[2]):
        day = data["date"].split('.')[0]
        month = data["date"].split('.')[1]
        year = data["date"].split('.')[2]
    elif (data["date"].split(',')[0] and data["date"].split(',')[1] and data["date"].split(',')[2]):
        day = data["date"].split(',')[0]
        month = data["date"].split(',')[1]
        year = data["date"].split(',')[2]
    sex = data["sex"]
    hour = data["date_born"].split(":")[0]
    minute = data["date_born"].split(":")[1]
    sec = "00"
    city = data["city"]
    chat_id = data["chat_id"]
    lat, lng, gmt = get_timezone(city)

    data_for_img1 = {
        "chart_info": 1,
        "only_other": 0,
        "style": "Северный",
        "type": "Стандартная карта",
        "view": "Стандартный",
        "divisionals": "D1",
        "general": "Знак",
        "other": '',
        "data": f'name={name}|date={day}.{month}.{year}|time={hour}:{minute}:{sec}|timezone={gmt}|latitude={lat}|longitude={lng}',
        "natal": f'name={name}|date={day}.{month}.{year}|time={hour}:{minute}:{sec}|timezone={gmt}|latitude={lat}|longitude={lng}',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'fr-BE,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    headers_for_img = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Dnt': '1',
        'Host': 'vedic-horo.ru',
        'Origin': 'https://vedic-horo.ru',
        'Referer': 'https://vedic-horo.ru/analyse.php',
        'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not;A;Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    url = f'https://vedic-horo.ru/analyse.php?name={name}&date={day}.{month}.{year}&time={hour}:{minute}:00&latitude={lat}&longitude={lng}&timezone={gmt}'
    with requests.Session() as session:
        auth_response_text = send_request(session, url, headers=headers, timeout=60)
        if auth_response_text:
            params = {"url": url, "chat_id": chat_id}
            return get_img(params)

#print(handle({"name": "Марат", "sex": "М", "date": "12.12.2012", "date_born": "16:36", "city": "Самара", "chat_id":'285690209'}))
