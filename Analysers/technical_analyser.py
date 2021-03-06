

class TechnicalAnalyser:
    def __init__(self, config):
        self.indicators = {}
        self.config = config

    def calculate_indicators(self, data):
        self.indicators["RSI"] = self.calculate_rsi(data)

    def get_indicator(self, indicator):
        return self.indicators[indicator]

    def get_indicators(self):
        return self.indicators

    def calculate_rsi(self, data):
        peroid = int(self.config.get_cfg("RSI_peroid"))
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
