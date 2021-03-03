from bs4 import BeautifulSoup
from urllib.request import urlopen


class Scraper:
    def __init__(self):
        self.soup = None
        self.path = ""

    def create_path(self, phrase):
        path_root = "https://www.bing.com/news/search?q="
        for text in phrase.split():
            path_root += text + "+"
        path_root = path_root[:-1]

        self.path = path_root + '&qft=sortbydate%3d"1"&form=YFNR&setmkt=en-US'

    def open(self):
        with urlopen(self.path) as url:
            try:
                self.soup = BeautifulSoup(url, 'html.parser')
            except Exception:
                print("Cant open site :(")

    def get_titles(self, company):
        titles = []
        self.create_path(company)
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
        self.titles_ = []
        self.update_headers()

    def get_company_phrases(self):
        pass

    def filter_phrases(self):
        pass

    def update_headers(self):
        sc = Scraper()
        self.titles_.extend(sc.get_titles(self.company))

    def get_headers(self):
        return self.titles_
