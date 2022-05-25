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


        r = self.session.get("https://lolz.guru/online/")
        soup = BeautifulSoup(r.text, "lxml")

        with open("index.html", "w", encoding="utf-8") as file: file.write(str(r.text))

        max_page = soup.find("div", {"class" : "PageNav"}).get("data-last")
        random_page = random.randint(1, int(max_page))

        time.sleep(1.5)

        r = self.session.get(f"https://lolz.guru/online/?page={random_page}")

        users = []
        articles = soup.find_all("a", {"class" : "username"})
        with open("ignore.txt", "r", encoding="utf-8") as file:
            ignore = file.read().split("\n")

        for article in articles:
            if article.get("href") in ignore:
                logger.error(f"Этот аккаунт я уже парсил: {article['href']}")
            else:
                users.append(article.get("href"))
                with open("ignore.txt", "a", encoding="utf-8") as file:
                    file.write(f"{article.get('href')}\n")

        return users

    def Spam(self):


        while True:

            users = self.Users()

            for user in users:
                try:
                    r = self.session.get(f"https://lolz.guru/{user}")
                    soup = BeautifulSoup(r.text, "lxml")

                    xfToken = soup.find("input", {"name" : "_xfToken"}).get("value")
                    

                    nickname = ""
                    if "members/" in user:
                        nickname = str(user).split("/")[1].replace("/", "")

                    else:
                        nickname = str(user).replace("/", "")
                    

                    self.session.get(f"https://lolz.guru/{nickname}/follow?_xfToken={xfToken}_xfRequestUri=%2Fsendreport%2F&_xfNoRedirect=1&_xfToken={xfToken}_xfResponseType=json").text
                    self.session.post(f"https://lolz.guru/{user}/follow", data={"_xfToken" : xfToken, "_xfConfirm": 1})

                    logger.success(f"Подписался на пользователя: {nickname}")
                    time.sleep(2)

                    with open("index.html", "w", encoding="utf-8") as file: file.write(str(r))

                except:
                    time.sleep(2)
                    logger.critical(f"Не смог оставить сообщение на стенке у https://lolz.guru/{user}")

lolz = LOLZTEAM()
lolz.AddCookie()
lolz.Spam()