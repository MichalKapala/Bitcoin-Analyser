import numpy as np


class TechnicalIndicators:
    def __init__(self):
        self.indicators_ = {}

    def update_indicators(self, data):
        self.indicators_.clear()
        self.indicators_["RSI"] = self.calculate_rsi(data)
        self.indicators_["Moving_average"] = self.calculate_moving_average(data)
        self.indicators_["Bollinger_bands"] = self.calculate_bb(data)

    def get_indicators(self, indicators_list):
        output = {}
        if indicators_list:
            output = {indicator: self.indicators_[indicator] for indicator in indicators_list}
        return output

    def calculate_bb(self, data):
        ma = self.indicators_["Moving_average"]
        no_elements = 20
        bb_h = []
        bb_d = []

        for i in range(no_elements, len(data), 1):
            mean = ma[i-no_elements]
            values = data["Close"][i-no_elements:i]
            std_dev = values.std()
            bb_d.append(mean - 2*std_dev)
            bb_h.append(mean + 2*std_dev)

        return np.array([bb_d, bb_h])

    @staticmethod
    def calculate_moving_average(data):
        no_elements = 20
        moving_average_list = []
        for i in range(no_elements, len(data), 1):
            values = data["Close"][i - no_elements:i]
            mean = values.mean()
            moving_average_list.append(mean)
        out = np.array(moving_average_list)

        return out

    @staticmethod
    def calculate_rsi(data):
        peroid = 14
        up = 0
        down = 0
        up_iter = 0
        down_iter = 0

        for i in range(peroid + 1, 2, -1):
            actual_close = data["Close"][-i]
            next_close = data["Close"][-i + 1]
            diff = next_close - actual_close
            if diff > 0:
                up_iter += 1
                up += diff
            else:
                down_iter += 1
                down += abs(diff)

        mean_up = up / up_iter
        mean_down = down / down_iter
        rs = mean_up / mean_down
        rsi = 100 - (100 / (1+rs))

        return rsi
