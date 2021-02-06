from text_anaylser import TextAnalyser

class Analyser:
    def __init__(self, path):
        self.text_analyser = TextAnalyser(path)

    def process(self):
        titles_evaluation = self.text_analyser.calculate_titles_values()