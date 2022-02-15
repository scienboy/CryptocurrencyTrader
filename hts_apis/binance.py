import ccxt
from datetime import datetime
import pandas as pd
import os
from PyQt5.QtCore import QMutex

import src.settings


class BinanceAPI():
    def __init__(self):
        self.mutex = QMutex()
        # # 기존 코드
        # self.binance = ccxt.binance

        # API key 조회
        with open(".\\data\\Binance_API\\api.txt") as f:
            lines = f.readlines()
            api_key = lines[0].strip()
            secret = lines[1].strip()

        # API key를 통해 binance 객체생성
        self.binance = ccxt.binance(config={
            'apiKey': api_key,
            'secret': secret
        })

        # self.get_ohlc_1m()

    def add_api_parse_cnt(self):
        self.mutex.lock()
        src.settings.myList['api_parse_cnt_binance'] = src.settings.myList['api_parse_cnt_binance'] + 1
        self.mutex.unlock()

    def parse_ohlcv(self, ticker, payment_currency="USDT", timeframe="1d"):
        self.add_api_parse_cnt()
        symbol = str(ticker) + '/' + str(payment_currency)
        ohlcv = pd.DataFrame(self.binance.fetch_ohlcv(symbol, timeframe))
        ohlcv.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
        ohlcv['time'] = ohlcv.apply(self.get_time, axis=1)

        return ohlcv




    def parse_current_price(self, ticker):
        self.add_api_parse_cnt()
        input_ticker = str(ticker) + '/' + "USDT"
        return self.binance.fetch_ticker(input_ticker)['close']




    def read_wallet_spot(self):
        return self.binance.fetch_balance()

    def read_wallet_future(self):
        return self.binance.fetch_balance(params={"type": "future"})

    def read_wallet_history(self):

        # transactions = self.binance.parse_orders()
        # transactions = self.binance.fetch_orders()
        # transactions = self.binance.parse_order_status()
        # transactions = self.binance.fetch_closed_orders()
        # transactions = self.binance.fetch_order_status()
        # transactions = self.binance.create_limit_buy_order
        return 0

    def generating_ohlcv_files(self, retry_cnt, root_dir, quote='USDT'):
        timeframes = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

        currencies = self.binance.fetch_currencies()
        markets = pd.DataFrame(self.binance.fetch_markets())
        coins_tg = markets[markets['quote'] == quote]

        # for base, symbol in quote_is_usdt_markets['base', 'symbol']:
        for i in coins_tg.index:
            try:
                dir_tg = root_dir + '\\' + quote + '\\' + str(coins_tg['base'][i])
                os.mkdir(dir_tg)
            except:
                print("Folder is exist!")

            for timeframe in timeframes:

                retry_cnt = 1

                ohlcv = pd.DataFrame(self.binance.fetch_ohlcv(coins_tg['symbol'][i], timeframe))
                ohlcv.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
                ohlcv['time'] = ohlcv.apply(self.get_time, axis=1)

                file_tg = dir_tg + "\\" + str(coins_tg['base'][i]) + "_candlestick_" + str(timeframe) + ".csv"

                try:
                    if os.path.isfile(file_tg):
                        print(file_tg + ' file is already exist!!!!!!!!!!!!!!!')
                        self.update_ohlcv_files(file_tg, ohlcv)
                    else:
                        ohlcv.to_csv(file_tg)
                except:
                    print('Retry generating ' + str(retry_cnt) + ' of ' + file_tg)
                    retry_cnt = retry_cnt + 1
                    if retry_cnt < 300:
                        self.generating_ohlcv_files(retry_cnt)
                    else:
                        print('Parsing skipped...   ' + file_tg)

    def update_ohlcv_files(self, file_tg, ohlcv):
        df = pd.read_csv(file_tg)
        a = df.iloc[-1].time
        b = ohlcv

    def get_time(self, df):
        return datetime.fromtimestamp(df['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

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