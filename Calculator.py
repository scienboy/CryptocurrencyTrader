import pybithumb

class Calculator():
    def __init__(self):
        pass

    # def get_mean_of_ohlc(self, ticker):



    def get_market_infos(self, ticker):
        try:
            df = pybithumb.get_ohlcv(ticker)
            ma5 = df['close'].rolling(window=5).mean()

            price = pybithumb.get_current_price(ticker)
            last_ma5 = ma5[-2]

            state = None
            if price > last_ma5:
                state = "상승장"
            else:
                state = "하락장"

            return (price, last_ma5, state)
        except:
            return (None, None, None)
