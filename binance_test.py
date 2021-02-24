import ccxt
from datetime import datetime

class BinanceAPI():
    def __init__(self):
        self.binance = ccxt.binance()
        self.get_ohlc_1m()

        pass

    def get_tickers(self):
        markets = self.binance.fetch_tickers()
        print(markets.keys())

    def get_ohlc_from_markets(self):
        markets = self.binance.fetch_tickers()
        print(markets.keys())
        for market in markets:
            ticker = self.binance.fetch_ticker(market)  # 전체 마켓 조회
            print(market, ticker['open'], ticker['high'], ticker['low'], ticker['close'])

    def get_ohlc_1m(self):
        ohlcvs = self.binance.fetch_ohlcv('ETH/BTC', "1m")
        # print(ohlcvs)
        for ohlc in ohlcvs:
            print(datetime.fromtimestamp(ohlc[0]/1000).strftime('%Y-%m-%d %H:%M:%S'))




# print(markets.keys())