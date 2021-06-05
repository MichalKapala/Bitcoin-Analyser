import numpy as np


class TechnicalIndicators:

    def __init__(self):
        self.indicators_ = {}
        self.no_elements = 20

    def update_indicators(self, data):
        self.indicators_.clear()
        self.indicators_["RSI"] = self.calculate_rsi(data)
        self.indicators_["Moving_average"] = self.calculate_moving_average(data)
        self.indicators_["Bollinger_bands"] = self.calculate_bb(data)
        self.indicators_["Weighted_MA"] = self.calculate_weighted_moving_average(data)
        self.indicators_["Exp_MA"] = self.calculate_exp_moving_average(data)

    def get_indicators(self, indicators_list):
        output = {}
        if indicators_list:
            output = {indicator: self.indicators_[indicator] for indicator in indicators_list}
        return output

    def calculate_bb(self, data):
        ma = self.indicators_["Moving_average"]
        bb_h = []
        bb_d = []

        for i in range(self.no_elements, len(data), 1):
            mean = ma[i-self.no_elements]
            values = data["Close"][i-self.no_elements:i]
            std_dev = values.std()
            bb_d.append(mean - 2*std_dev)
            bb_h.append(mean + 2*std_dev)

        return np.array([bb_d, bb_h])

    def calculate_moving_average(self, data):
        moving_average_list = []
        for i in range(self.no_elements, len(data), 1):
            values = data["Close"][i - self.no_elements:i]
            mean = values.mean()
            moving_average_list.append(mean)
        out = np.array(moving_average_list)

        return out

    def calculate_weighted_moving_average(self, data):
        weighted_moving_average_list = []
        for i in range(self.no_elements, len(data), 1):
            sum = 0
            weights = 0
            for j in range(0, self.no_elements, 1):
                sum += j*data["Close"][i-j]
                weights += j
            weighted_moving_average_list.append(sum / weights)

        out = np.array(weighted_moving_average_list)

        return out

    def calculate_exp_moving_average(self, data):
        exp_moving_average_list = []
        alfa = 2 / (self.no_elements + 1)
        for i in range(self.no_elements, len(data), 1):
            sum = 0
            weights = 0
            for j in range(0, self.no_elements, 1):
                current_scalar = (1-alfa)**j
                sum += current_scalar*data["Close"][i-j]
                weights += current_scalar
            exp_moving_average_list.append(sum / weights)

        out = np.array(exp_moving_average_list)

        return out

    def calculate_rsi(self, data):
        up = 0
        down = 0
        up_iter = 0
        down_iter = 0

        for i in range(self.no_elements + 1, 2, -1):
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
