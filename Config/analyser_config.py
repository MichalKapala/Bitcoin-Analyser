
PATH = "C:/Users/Michal/PycharmProjects/Stock/Config/config.txt"

class AnalyserConfig:
    def __init__(self):
        self.config_dict = {}
        self.set_config()

    def set_config(self):
        file = open(PATH)
        for line in file:
            line = line.rstrip()
            if line:
                params = line.split(" ")
                self.config_dict[params[0]] = params[1]

    def get_cfg(self, property):
        return self.config_dict[property]


