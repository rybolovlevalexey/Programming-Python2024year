import requests
from bs4 import BeautifulSoup
import pickle
import os
from pprint import pprint


class MySession:
    auth_url = "https://www.comtt.ru/"
    search_url = "https://www.comtt.ru/search.php"
    auth_data = {"username": "", "password": ""}
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
        resp = check_session.get(self.search_url)
        soup = BeautifulSoup(resp.content, "html.parser")
        if ("Внимание! Вы не авторизованы!" in
                list(elem.text.strip() for elem in soup.find_all("p"))):
            return False
        return resp.status_code == 200

    def exists_session_info(self) -> bool:
        return os.path.exists(self.session_file)

    def session_ready_without_files(self):
        self.cur_session = requests.Session()
        cur_session_resp = self.cur_session.post(self.auth_url, data=self.auth_data)

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

        cur_session_resp = self.cur_session.post(self.auth_url, data=self.auth_data)
        if cur_session_resp.status_code == 200:
            print("Создана новая актуальная сессия, и она сохранена в файл")
            self.save_session()
            return True
        print("Создана новая сессия, но произошла ошибка при авторизации")
        return False

    def search_product_by_article(self, article: str):
        search_response = self.cur_session.get(self.search_url, params={'fnd': article})
        soup = BeautifulSoup(search_response.content, "html.parser")


if __name__ == "__main__":
    session = MySession()
    session.session_ready_to_work()
