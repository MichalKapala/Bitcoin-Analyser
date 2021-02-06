from scraper import Scraper


class TextAnalyser:
    def __init__(self, path):
        self.path = path
        self.titles = []

    def calculate_titles_values(self):
        titles_sum = 0
        sc = Scraper()
        sc.open(self.path)
        titles = sc.get_titles()
        for title in titles:
            titles_sum += self.title_evaluation(title)

    def title_evaluation(self, title):
        return 0
