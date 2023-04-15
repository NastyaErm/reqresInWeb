import json
import time
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

path = "C:\\chromedriver.exe"
s = Service(path)
driver = webdriver.Chrome(service=s)


def test_api_result_matches_web_result():
    #Запрос API
    api_response = requests.get('https://reqres.in/api/users/2')
    api_status_code = api_response.status_code
    api_body = api_response.json()

    #Открываем главную страницу, клик на кнопку
    driver.get('https://reqres.in/')
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0, 800);")
    button = driver.find_element(By.XPATH, "//li[@data-id='users-single']//a[contains(text(),'Single user')]")
    button.click()
    time.sleep(2)

    #Видим результаты на странице
    web_status_code = driver.find_element(By.XPATH, "//span[@data-key='response-code']")
    web_body = driver.find_element(By.XPATH, "//pre[@data-key='output-response']")
    web_status_code = int(web_status_code.text)
    web_body = web_body.text.strip()

    driver.quit()

    #Проверка статусов и ответов api и web
    assert api_status_code == web_status_code

    sorted_body_api = json.dumps(api_body, sort_keys=True)
    sorted_body_web = json.dumps(json.loads(web_body), sort_keys=True)
    assert sorted_body_api == sorted_body_web



