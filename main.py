from Analysers.analyser import Analyser


company = "CD projekt RED"

if __name__ == "__main__":
    main_analyser = Analyser(company)
    main_analyser.process()