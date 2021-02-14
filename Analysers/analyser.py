from Analysers.text_anaylser import TextAnalyser


class Analyser:
    def __init__(self, company):
        self.company = company
        self.text_analyser = TextAnalyser(company)

    def process(self):
        titles_evaluation = self.text_analyser.calculate_titles_values()