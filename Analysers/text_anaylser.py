from Scraper.scraper import Headers


class TextAnalyser:
    def __init__(self, company):
        self.company = company
        self.titles = []
        self.update_titles()

    def update_titles(self):
        hd = Headers(self.company)
        hd.update_headers()

    def calculate_titles_values(self):
        self.update_titles()

    def title_evaluation(self, title):
        pass
