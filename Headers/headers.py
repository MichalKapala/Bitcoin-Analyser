from bs4 import BeautifulSoup
from urllib.request import urlopen
import sqlite3
from datetime import datetime

class Scraper:
    def __init__(self, company):
        self.soup = None
        self.company = company
        self.path = ""

    def create_path(self):
        path_root = "https://www.bing.com/news/search?q="
        for text in self.company.split():
            path_root += text + "+"
        path_root = path_root[:-1]

        self.path = path_root + '&qft=sortbydate%3d%221%22&form=YFNR'

    def open(self):
        with urlopen(self.path) as url:
            try:
                self.soup = BeautifulSoup(url, 'html.parser')
            except:
                print("Cant open site :(")

    def get_titles(self):
        titles = []
        self.create_path()
        self.open()

        if self.soup is not None:
            self.soup = self.soup.body.find("div", {"class": "main-container"})
            news = self.soup.findAll("div", {"class": "news-card newsitem cardcommon b_cards2"})
            for n in news:
                titles.append(n.find("a", {"class": "title"}).text)
        else:
            print("Nie udalo sie pobrac naglowkow")
        return titles

class Headers:
    def __init__(self, company):
        self.company = company
        self.update_headers()

    def update_headers(self):
        sc = Scraper(self.company)
        titles = sc.get_titles()
        if titles:
            self.save_titles(titles)

    def save_titles(self, titles):
        connect = sqlite3.connect("headers.db")
        c = connect.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS headers (company text, date text, header text unique)''')
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        for title in titles:
            c.execute('''INSERT OR IGNORE INTO headers VALUES (?,?,?)''', (self.company, dt_string, title))
        connect.commit()
        connect.close()

    def get_headers_in_time(self, time_start, time_end):
        pass
