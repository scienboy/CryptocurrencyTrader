import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QMutex
from .binance import *
import pykorbit
import pybithumb
import time

import src.settings
# import datetime

# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

form_class_old = uic.loadUiType("ui/1stDesign.ui")[0]
form_class_bull = uic.loadUiType("ui/bull.ui")[0]
form_class_myscreen = uic.loadUiType("ui/myScreen_01.ui")[0]
tickers = ["BTC", "ETH", "BCH", "ETC"]

api_parse_cnt = 0

class MyWindowBull(QMainWindow, form_class_bull):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.tickers = pybithumb.get_tickers()
        self.tickers = ["BTC", "ETH", "BCH", "ETC"]
        self.all = pybithumb.get_current_price("ALL")        # 한 번에 최대한 많은 정보 조회

        timer = QTimer(self)
        timer.start(1)        # 1초마다 반복
        timer.timeout.connect(self.set_data)

    def set_data(self):

        Bithumb = BithumbAPI()
        for i, ticker in enumerate(self.tickers):
            price, last_ma5, state = Bithumb.bull_market(ticker)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(ticker))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(price)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(last_ma5)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(state))

    # def set_data(self):
    #
    #     for ticker in self.tickers:
    #          is_bull = Bithumb.bull_market(ticker)
    #     if is_bull:
    #         print(ticker, "상승장")
    #     else:
    #         print(ticker, "하락장")

class MyWindowOld(QMainWindow, form_class_old):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        btn = QPushButton("버튼1", self)      # UI에 내용 덮어씀
        btn.move(10, 10)
        btn.clicked.connect(self.btn_clicked)

        self.timer = QTimer(self)
        self.timer.start(1000)      # 1000: interval를 1초에 한 번
        self.timer.timeout.connect(self.inquiry)            # timeout(1초) 마다 한 번씩 inquiry함수 호출
        # self.pushButton.clicked.connect(self.inquiry)       # 버튼을 누를 때 마다 inquiry 함수 호출

        mysignal = MySignal()
        mysignal.signal1.connect(self.signal1_emitted)  # 내가 생성한 signal을 함수와 연결시킴
        mysignal.signal2.connect(self.signal2_emitted)  # 내가 생성한 signal을 함수와 연결시킴
        mysignal.run()

    def signal1_emitted(self):
        print("signal1 emitted")

    def signal2_emitted(self, arg1, arg2):
        print("signal2 emitted", arg1, arg2)

    def inquiry(self):
        cur_time = QTime.currentTime()
        str_time = cur_time.toString("hh:mm:ss")
        self.statusBar().showMessage(str_time)
        price = pykorbit.get_current_price("BTC")
        self.lineEdit.setText(str(price))

    def timeout(self):
        cur_time = QTime.currentTime()
        str_time = cur_time.toString("hh:mm:ss")
        self.statusBar().showMessage(str_time)

    def btn_clicked(self):
        print("버튼 클릭")

class MyWindowTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 200, 300, 200)
        self.setWindowTitle("PyQt")
        self.setWindowIcon(QIcon("../image/iconfinder_cryptocurrency_blockchain_Bitcoin_BTC_2907507.png"))

        btn = QPushButton("버튼1", self)
        btn.move(10, 10)
        btn.clicked.connect(self.btn_clicked)

        btn2 = QPushButton("버튼2", self)
        btn2.move(10, 40)

        # self().__init__()
        # pass
    def btn_clicked(self):
        print("버튼 클릭")

class MyWindowThread(QMainWindow, form_class_bull):
    def __init__(self, tickers):
        super().__init__()
        self.setupUi(self)          # form_class_bull로 들어온 .ui 파일을 반영함

        self.worker = Worker(tickers)
        self.worker.finished.connect(self.update_table_widget)
        self.worker.start()

    def update_table_widget(self, data):
        try:
            for ticker, infos in data.items():
                index = tickers.index(ticker)

                self.tableWidget.setItem(index, 0, QTableWidgetItem(ticker))
                self.tableWidget.setItem(index, 1, QTableWidgetItem(str(infos[0])))
                self.tableWidget.setItem(index, 2, QTableWidgetItem(str(infos[1])))
                self.tableWidget.setItem(index, 3, QTableWidgetItem(str(infos[2])))
        except:
            pass

class MyWindow_new(QMainWindow, form_class_myscreen):
    def __init__(self, tickers):
        super().__init__()
        self.setupUi(self)

        # btn = QPushButton("pushButton_01", self)      # UI에 내용 덮어씀
        # btn.move(10, 10)
        # btn.clicked.connect(self.btn_clicked)

        # btn = QPushButton("pushButton_01", self)

        # self.tableWidget.setRowCount(len(tickers))
        self.worker = Worker2(tickers)
        self.worker.finished.connect(self.update_table_widget)
        self.worker.start()

        self.pushButton_01.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        print("버튼 클릭")
        # self.tableWidget.setItem(6, 1, QTableWidgetItem(str(binance_test.read_wallet)))
        binance_test = BinanceAPI()
        balance = binance_test.read_wallet_spot()
        self.tableWidget.setItem(6, 0, QTableWidgetItem(str(balance['BTC']['total'])))


    # @pyqtSlot(dict)
    def update_table_widget(self, data):
        try:
            for ticker, infos in data.items():
                index = tickers.index(ticker)

                self.tableWidget.setItem(index, 0, QTableWidgetItem(ticker))
                self.tableWidget.setItem(index, 1, QTableWidgetItem(str(infos[0])))
                self.tableWidget.setItem(index, 2, QTableWidgetItem(str(infos[1])))
                self.tableWidget.setItem(index, 3, QTableWidgetItem(str(infos[2])))
        except:
            pass


class MySignal(QObject):
    signal1 = pyqtSignal()
    signal2 = pyqtSignal(int, int)

    def run(self):
        self.signal1.emit()
        self.signal2.emit(1, 2)

class BithumbAPI():
    def __init__(self):
        self.mutex = QMutex()
        pass

    def parse_ohlcv(self, ticker, payment_currency="KRW", timeframe="1d"):
        if timeframe == '1d':
            timeframe = 'day'
        return pybithumb.get_ohlcv(ticker, payment_currency, timeframe)

    def add_api_parse_cnt(self):
        self.mutex.lock()
        src.settings.myList['api_parse_cnt_bithumb'] = src.settings.myList['api_parse_cnt_bithumb'] + 1
        self.mutex.unlock()

    def parse_current_price(self, ticker):
        self.add_api_parse_cnt()
        return pybithumb.get_current_price(ticker)

    def parse_detail(self):
        tickers = pybithumb.get_tickers()

        for ticker in tickers:
            # price = pybithumb.get_current_price(ticker)   # 현재가 조회
            detail = pybithumb.get_market_detail(ticker)    # 저가, 고가, 평균 거래 금액, 거래량
            print(ticker, detail)

            orderbook = pybithumb.get_orderbook(ticker)     # 시점, 거래화폐, 코인명, 매도호가, 매수호가
            print(orderbook["order_currency"] + " / " + orderbook["payment_currency"], datetime.datetime.fromtimestamp(int(orderbook["timestamp"])/1000))
            for bid in orderbook['bids']:
                print("매수호가: ", bid['price'], "매수잔량: ", bid['quantity'])
            for ask in orderbook['asks']:
                print("매도호가: ", bid['price'], "매도잔량: ", bid['quantity'])

            time.sleep(0.1)

    def parse_all(self):
        all = pybithumb.get_current_price("ALL")        # 한 번에 최대한 많은 정보 조회
        # for key, value in all.items():
        #     print(key, value)
            # Key           	Description
            # opening_price	    최근 24시간 내 시작 거래금액
            # closing_price	    최근 24시간 내 마지막 거래금액
            # min_price         최근	24시 간 내 최저 거래금액
            # max_price         최근	24시 간 내 최고 거래금액
            # average_price	    최근 24시간 내 평균 거래금액
            # units_traded	    최근 24시간 내 Currency 거래량
            # volume_1day	    최근 1일간 Currency 거래량
            # volume_7day	    최근 7일간 Currency 거래량
            # buy_price	        거래 대기건 최고 구매가
            # sell_price	    거래 대기건 최소 판매가
            # 24H_fluctate	    24시간 변동금액
            # 24H_fluctate_rate	24시간 변동률
        for ticker, data in all.items():
            print(ticker, data['closing_price'])        # 모든 가상화폐의 현재가 출력

    def bull_market(self, ticker):
        ohlcv_btc = pybithumb.get_ohlcv(ticker, "KRW", "day")
        ma5 = ohlcv_btc['close'].rolling(window=5).mean()       # 5일 이동평균선 연산.
        price = pybithumb.get_current_price(ticker)
        last_ma5 = ma5[-2]

        state = None
        if price > last_ma5:
            state = "상승장"
        else:
            state = "하락장"

        return price, last_ma5, state

class Worker(QThread):
    
    finished = pyqtSignal(dict)

    def __init__(self, tickers):
        super().__init__()
        # self.finished = pyqtSignal(dict)        # 사용자 정의 시그널(이벤트) 객체 생성
        self.tickers = tickers

    def run(self):
        while True:
            data = {}

            for ticker in self.tickers:
                data[ticker] = self.get_market_infos(ticker)

            self.finished.emit(data)
            # print(data)
            time.sleep(1)

    def get_market_infos(self, ticker):
        try:
            df = pybithumb.get_ohlcv(ticker)
            ma5 = df['close'].rolling(window=5).mean()
            last_ma5 = ma5[-2]
            price = pybithumb.get_current_price(ticker)

            state = None
            if price > last_ma5:
                state = "상승장"
            else:
                state = "하락장"
            return price, last_ma5, state
        except:
            return None, None, None

class Worker2(QThread):

    finished = pyqtSignal(dict)

    def __init__(self, tickers):
        super().__init__()
        # self.finished = pyqtSignal(dict)
        self.tickers = tickers

    def run(self):
        while True:
            data = {}

            for ticker in tickers:
                data[ticker] = self.get_market_infos(ticker)

            self.finished.emit(data)
            self.msleep(500)

    def get_market_infos(self, ticker):
        try:
            df = pybithumb.get_ohlcv(ticker)
            ma5 = df['close'].rolling(window=5).mean()
            last_ma5 = ma5[-2]
            price = pybithumb.get_current_price(ticker)

            state = None
            if price > last_ma5:
                state = "상승장"
            else:
                state = "하락장"

            return price, last_ma5, state
        except:
            return None, None, None
