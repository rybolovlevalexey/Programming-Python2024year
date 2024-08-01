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
    with open("комтранс_авторизация.txt", "r") as auth_data_file:
        username_omega = auth_data_file.readline().strip()
        password_omega = auth_data_file.readline().strip()
        auth_data = {"username": username_omega,
                     "password": password_omega}
        auth_data_v2 = {"login": username_omega,
                        "pass": password_omega}
    user_agent = UserAgent().random


class ParserComTrans:
    session_file = 'session.pkl'

    def __init__(self):
        self.cur_session = requests.Session()

    def save_session(self):
        with open(self.session_file, 'wb') as file:
            cookies_info = list({"domain": key.domain, "name": key.name,
                                 "path": key.path, "value": key.value}
                                for key in self.cur_session.cookies)
            pickle.dump({
                "cookies": cookies_info,
                "headers": self.cur_session.headers,
            }, file)
        print("Выполнено сохранение информации о текущей сессии")

    def load_session_from_file(self):
        self.cur_session = requests.Session()
        with open(self.session_file, 'rb') as file:
            data = pickle.load(file)
            for cook in data["cookies"]:
                self.cur_session.cookies.set(**cook)
            self.cur_session.headers.update(data["headers"])
        print("Выполнена выгрузка информации о прошедшей сессии в текущую")

    @staticmethod
    def is_logged_in(check_session) -> bool:
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
                                                 data=InfoRequest.auth_data_v2,
                                                 headers={"User-Agent": InfoRequest.user_agent})
        print(BeautifulSoup(cur_session_resp.content, "html.parser").prettify())
        print("Создана новая сессия и выполнена её авторизация")

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

        cur_session_resp = self.cur_session.post(InfoRequest.auth_url,
                                                 data=InfoRequest.auth_data_v2)
        if cur_session_resp.status_code == 200:
            if "ОМЕГА ТРАК ООО" in cur_session_resp.text:
                print("Создана новая сессия и выполнена её авторизация")
                self.save_session()
                print("Информация об этой сессии перезаписана в файл")
            else:
                print("Создана новая сессия, но НЕ выполнена её авторизация")
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


def func_timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func_result = func(*args, **kwargs)
        end_time = time.time()
        result_time = end_time - start_time
        print(f"Время выполнения запроса {result_time:.4f} секунд")
        return func_result
    return wrapper


@func_timer
def main_selenium(article: str):
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
        driver.get(InfoRequest.search_url + f"?fnd={article}")
        print("выполнение поиска по артикулу")

        # Ожидание загрузки защищенной страницы
        time.sleep(3)
        print("страница загружена")

        # Парсинг содержимого защищенной страницы
        print("начат парсинг")
        content = driver.find_element(By.TAG_NAME, 'body')
        tag_name = "tbody"
        class_name = "sort"
        # print(len(content.find_elements(By.CSS_SELECTOR, f"{tag_name}.{class_name}")))
        info_by_article = list()
        for line in content.find_element(By.CSS_SELECTOR, f"{tag_name}.{class_name}").find_elements(
                By.TAG_NAME, "tr"):
            info_by_article.append([line.find_elements(By.TAG_NAME, "td")[1].text.strip(),
                                    line.find_elements(By.TAG_NAME, "td")[2].text.strip(),
                                    line.find_elements(By.TAG_NAME, "td")[6].text.strip()])
        print(f"Кол-во товаров найденных по артикулу {len(info_by_article)}")
        info_by_article = list(filter(lambda info_part: info_part[0] == article, info_by_article))
        print(f"Кол-во товаров с точным соответствием артикула {len(info_by_article)}")
        info_by_article = sorted(info_by_article, key=lambda info_part: info_part[2])
        pprint(info_by_article)
        print(f"Самая низкая цена - {info_by_article[0][2]} \n"
              f"самая высокая цена - {info_by_article[-1][2]}")

    finally:
        # Закрытие WebDriver
        driver.quit()


if __name__ == "__main__":
    # parser = ParserComTrans()
    # parser.session_ready_to_work()
    main_selenium("85696")
