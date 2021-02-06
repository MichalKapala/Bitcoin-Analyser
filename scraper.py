from bs4 import BeautifulSoup
from urllib.request import urlopen

class Scraper:
    def __init__(self):
        self.soup = None

    def open(self, path):
        with urlopen(path) as url:
            try:
                self.soup = BeautifulSoup(url, 'html.parser')
            except:
                print("Cant open site :(")

    def get_titles(self):
        titles = []
        if self.soup is not None:
            self.soup = self.soup.body.find("div", {"class": "main-container"})
            news = self.soup.findAll("div", {"class": "news-card newsitem cardcommon b_cards2"})
            for n in news:
                titles.append(n.find("a", {"class": "title"}).text)
        return titles



