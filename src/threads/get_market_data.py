from PyQt5.QtCore import QMutex
from src.hts_apis.bithumb import *
from src.hts_apis.binance import *

class Thread_get_market_data(QThread):

    finished_table_row = pyqtSignal(list)

    def __init__(self, hts='Binance', currency='KRW', ticker='BTC', row=0):
        super().__init__()
        self.hts = hts
        self.ticker = ticker
        self.row = row
        self.mutex = QMutex()
        self.currency = currency


        if self.hts == 'Bithumb':
            self.hts_api = BithumbAPI()
        elif self.hts == 'Binance':
            self.hts_api = BinanceAPI()

    def run(self):

        while True:

            time_init = datetime.now()

            if self.hts == 'Bithumb':
                current_price = self.hts_api.parse_current_price(self.ticker)
                ohlcv = self.hts_api.parse_ohlcv(self.ticker, self.currency, "1d")  # Bithumb KRW 기준
            elif self.hts == 'Binance':
                current_price = self.hts_api.parse_current_price(self.ticker)
                ohlcv = self.hts_api.parse_ohlcv(self.ticker, self.currency, "1d")    # Binance USD 기준

            time_end = datetime.now()
            duration = time_end - time_init

            last_ma_n, state = self.get_ma_state(current_price, ohlcv, criteria = 'close', n = 5)

            self.finished_table_row.emit([self.row, self.ticker, current_price, last_ma_n, state, duration.microseconds/1000000, time_end])
            self.msleep(500)


    # ohlcv 중 기준값(criteria)에 따른 n일 이평선과 상승장/하락장 판별결과 return함수
    def get_ma_state(self, current_price, ohlcv, criteria, n):
        try:
            ma = ohlcv['close'].rolling(window=5).mean()

            last_ma = ma[len(ma) - 2]

            state = None
            if current_price > last_ma:
                state = "상승장"
            else:
                state = "하락장"

            return last_ma, state
        except:
            print('wtf2')
            return None, None

