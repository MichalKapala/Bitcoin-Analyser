from analyser import Analyser

PATH = 'https://www.bing.com/news/search?q=cd+projekt+red&qft=sortbydate%3d%221%22&form=YFNR'

if __name__ == "__main__":
    main_analyser = Analyser(PATH)
    main_analyser.process()