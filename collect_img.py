import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def get_img(params):
    data = params
    url = data["url"]
    chat_id = data["chat_id"]
    service = Service(executable_path="chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {"profile.default_content_settings.popups": 0,
            "download.default_directory":fr'{os.path.dirname(os.path.abspath(__file__))}/downloads', ### Set the path accordingly
            "download.prompt_for_download": False,
            "download.directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(service=service, options=options)
    browser.get(url)
    acs = browser.find_element(By.XPATH,'//*[@id="natal-info"]/table/tbody/tr[1]/td[4]')
    acs_text = acs.text
    time.sleep(1)
    moon = browser.find_element(By.XPATH,'//*[@id="natal-info"]/table/tbody/tr[3]/td[4]')
    moon_text = moon.text
    time.sleep(1)
    menu = browser.find_element(By.CLASS_NAME, 'menu-sub')
    menu.click()
    time.sleep(1)
    save_to = browser.find_element(By.ID, "chart-to-png")
    save_to.click()
    time.sleep(2)
    div_severny = browser.find_element(By.XPATH, '//*[@id="content"]/div[3]/div[3]')
    div_severny.click()
    time.sleep(2)
    div_znak = browser.find_element(By.XPATH, "//div[text()='Знак']")
    div_znak.click()
    div_input = browser.find_element(By.ID, 'png-name')
    div_input.clear()
    div_input.send_keys(f'{chat_id}' + Keys.RETURN)
    btn = browser.find_element(By.ID, 'chart-to-png-accept')
    btn.click()
    time.sleep(10)
    browser.close()
    browser.quit()
    os.system("pkill chromedriver")
    return acs_text, moon_text, chat_id

#print(get_img({"url":"https://vedic-horo.ru/analyse.php?name=Александр&date=11.05.1999&time=12:00:00&latitude=54.51&longitude=36.26&timezone=3", "chat_id":'285690209'}))
