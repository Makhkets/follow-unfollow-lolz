from logging import critical
import re
import time
import random
import config
import requests
from loguru import logger
from bs4 import BeautifulSoup
import json
from pprint import pprint


class LOLZTEAM():
    def __init__(self):
        self.session = requests.Session()

        self.headers = {
            'authority': 'lolz.guru',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://lolz.guru/forums/910/',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'if-modified-since': 'Fri, 01 Apr 2022 20:26:49 GMT',
        }
        self.session.headers.update(self.headers)

    def AddCookie(self):
        cookies = {}
        with open("cookies.json", "r", encoding="utf-8") as file: data = json.load(file)
        for i in data:
            cookies[i['name']] = i['value']

        logger.success("Успешно загрузил куки")
        self.session.cookies.update(cookies)

    def Users(self):

        # https: // lolz.guru / online /?page = 2


        r = self.session.get("https://lolz.guru/account/following")
        soup = BeautifulSoup(r.text, "lxml")

        with open("index.html", "w", encoding="utf-8") as file: file.write(str(r.text))

        users = []
        for user in soup.find_all('li', {"class" : "primaryContent memberListItem"}):
            users.append("https://lolz.guru/" + user.find("a").get("href"))

        logger.success(users)
        return users

    def Spam(self):

        for user in self.Users():
            try:

                soup = BeautifulSoup(self.session.get(user).text, "lxml")
                user_id = soup.find("div", {"class": "userContentLinks"}).find("a", {"button"}).get("href").split("user_id=")[1].split("&")[0]
                logger.success(f"user_id: {user_id}")

                r = self.session.post("https://lolz.guru/account/stop-following.json", data={
                    "user_id": user_id,
                    "_xfConfrim": 1,
                    "_xfRequestUri": "/account/following",
                    "_xfNoRedirect": 1,
                    "_xfToken": soup.find("input", {"name" : "_xfToken"}).get("value"),
                    "_xfResponseType": "json"
                }).json()

                print(r)
                logger.success("Отписался от: " + user)


            except Exception as ex: logger.critical(ex)

lolz = LOLZTEAM()
lolz.AddCookie()
lolz.Spam()
# lolz.Spam()