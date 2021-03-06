from Scraper.scraper import Headers


class TextAnalyser:
    def __init__(self, company):
        self.company = company
        self.titles = []
        self.update_titles()

    def update_titles(self):
        hd = Headers(self.company)
        hd.update_headers()
        self.titles = hd.get_headers()

    def get_titles(self):
        return self.titles

    def calculate_titles_values(self):
        pass

    def title_evaluation(self, title):
        pass
