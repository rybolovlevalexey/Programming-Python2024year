import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pickle
import os
from pprint import pprint
from requests.auth import HTTPBasicAuth
import time
from dataclasses import dataclass
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class InfoRequest:
    auth_url = "https://www.comtt.ru/login.php"
    search_url = "https://www.comtt.ru/search.php"
    # search_url_v2 = "https://www.comtt.ru/k/a/example/ws_search/search.php"
    search_url_v2 = "https://www.comtt.ru/k/t/t.php"
    auth_data = {"username": "", "password": ""}
    auth_data_v2 = {"login": "", "pass": ""}
    user_agent = UserAgent().random


class MySession:
    session_file = 'session.pkl'

    def __init__(self):
        self.cur_session = requests.Session()

    def save_session(self):
        with open(self.session_file, 'wb') as file:
            pickle.dump({
                'cookies': self.cur_session.cookies.get_dict(),
                'headers': self.cur_session.headers,
            }, file)

    def load_session_from_file(self):
        self.cur_session = requests.Session()
        with open(self.session_file, 'rb') as file:
            data = pickle.load(file)
            self.cur_session.cookies.update(data['cookies'])
            self.cur_session.headers.update(data['headers'])

    def is_logged_in(self, check_session) -> bool:
        resp = check_session.get(InfoRequest.search_url,
                                 headers={"User-Agent": InfoRequest.user_agent})
        soup = BeautifulSoup(resp.content, "html.parser")
        if ("Внимание! Вы не авторизованы!" in
                list(elem.text.strip() for elem in soup.find_all("p"))):
            return False
        return resp.status_code == 200

    def exists_session_info(self) -> bool:
        return os.path.exists(self.session_file)

    def session_ready_without_files(self):
        self.cur_session = requests.Session()
        print("Начата авторизация")
        cur_session_resp = self.cur_session.post(InfoRequest.auth_url,
                                                 data=InfoRequest.auth_data,
                                                 headers={"User-Agent": InfoRequest.user_agent})
        print(BeautifulSoup(cur_session_resp.content, "html.parser").prettify())
        print("Создана новая сессия и выполнена её авторизация")

    def session_ready_without_files_v2(self):
        self.cur_session = requests.Session()
        print("Начата авторизация")
        cur_session_resp = self.cur_session.post(InfoRequest.auth_url,
                                                 data=InfoRequest.auth_data_v2,
                                                 headers={"User-Agent": InfoRequest.user_agent})
        if "ОМЕГА ТРАК ООО" in cur_session_resp.text:
            print("Создана новая сессия и выполнена её авторизация")
        else:
            print("Создана новая сессия, но НЕ выполнена её авторизация")

    def making_session_another_version(self, article: str):
        self.cur_session = requests.Session()
        print("Начато выполнение запроса одновременно с авторизацией")
        cur_session_resp = self.cur_session.get(InfoRequest.search_url,
                                                auth=HTTPBasicAuth(
                                                    InfoRequest.auth_data["username"],
                                                    InfoRequest.auth_data["password"]),
                                                params={'fnd': article},
                                                headers={"User-Agent": InfoRequest.user_agent})
        print("Запрос выполнен одновременно с авторизацией")
        print(BeautifulSoup(cur_session_resp.content, "html.parser").prettify())

    def session_ready_to_work(self):
        if self.cur_session is requests.Session and self.cur_session != requests.Session():
            if self.is_logged_in(self.cur_session):
                print("Текущая сессия авторизована")
                return True
        else:
            if self.cur_session is not requests.Session:
                self.cur_session = requests.Session()
                print("Создана новая пустая сессия")
            elif self.cur_session == requests.Session():
                print("Сессия на данный момент является пустой")

        if self.exists_session_info():
            self.load_session_from_file()
            print("Найден файл с инфой о сессии")
        if self.is_logged_in(self.cur_session):
            print("Из найденного файла о сессии получены актуальные данные")
            return True

        cur_session_resp = self.cur_session.post(InfoRequest.auth_url, data=InfoRequest.auth_data)
        if cur_session_resp.status_code == 200:
            print("Создана новая актуальная сессия, и она сохранена в файл")
            self.save_session()
            return True
        print("Создана новая сессия, но произошла ошибка при авторизации")
        return False

    def search_product_by_article(self, article: str):
        search_response = self.cur_session.get(InfoRequest.search_url, params={"fnd": article},
                                               headers={"User-Agent": InfoRequest.user_agent},
                                               stream=True)
        time.sleep(20)
        soup = BeautifulSoup(search_response.content, "html.parser")
        print(soup.prettify())
        print(soup.find_all("tbody")[1])

    def search_product_by_article_v2(self, article: str):
        search_response = self.cur_session.post(InfoRequest.search_url_v2,
                                               data={'search': article},
                                               headers={"User-Agent": InfoRequest.user_agent,
                                                        "Content-Type":
                                                            "application/x-www-form-urlencoded"})
        soup = BeautifulSoup(search_response.content, "html.parser")
        print(soup.prettify())
        print("-------------------")
        # print(soup.find_all("tbody")[1])
        print(search_response.content)


def main_selenium():
    chrome_options = Options()
    chrome_options.add_argument(
        "--headless")  # Запуск браузера в фоновом режиме (без графического интерфейса)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print("До блока try нет никаких ошибок")

    try:
        # Открытие страницы авторизации
        driver.get(InfoRequest.auth_url)
        print("страница открыта успешно")

        # Поиск и заполнение полей для ввода логина и пароля
        username_field = driver.find_element(By.NAME, 'login')
        password_field = driver.find_element(By.NAME, 'pass')
        print("найдены поля логин и пароль")
        username_field.send_keys(InfoRequest.auth_data["username"])
        password_field.send_keys(InfoRequest.auth_data["password"])
        password_field.send_keys(Keys.RETURN)
        print("введены данные и нажат enter")

        # Ожидание загрузки страницы после авторизации
        time.sleep(3)
        print("страница загружена")

        # Переход к защищенной странице
        driver.get(InfoRequest.search_url + "?fnd=85696")
        print("выполнение поиска по артикулу")

        # Ожидание загрузки защищенной страницы
        time.sleep(3)
        print("страница загружена")

        # Парсинг содержимого защищенной страницы
        content = driver.find_element(By.CLASS_NAME, 'content')
        print("парсинг")
        print(content.text)

    finally:
        # Закрытие WebDriver
        driver.quit()


if __name__ == "__main__":
    session = MySession()
    session.session_ready_without_files_v2()
    session.search_product_by_article("85696")
