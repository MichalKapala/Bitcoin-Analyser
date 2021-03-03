from Analysers.analyser import Analyser

company_name = "Aptiv"
company_ticker = "APTV"

if __name__ == "__main__":
    main_analyser = Analyser(company_name, company_ticker)
    main_analyser.process()
