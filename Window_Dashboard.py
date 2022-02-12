import datetime

from bithumb_test import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class_old = uic.loadUiType("ui/1stDesign.ui")[0]
form_class_bull = uic.loadUiType("ui/bull.ui")[0]
form_class_myscreen = uic.loadUiType("ui/myScreen_01.ui")[0]
# tickers = ["BTC", "ETH", "BCH", "ETC", "GALA"]


api_parse_cnt_bithumb = 0
api_parse_cnt_binance = 0

class Window_Dashboard(QMainWindow, form_class_myscreen):
    def __init__(self, tickers):

        super().__init__()
        self.setupUi(self)
        self.thread_runner_table()

        # binance 지갑 관련 정보 조회
        self.worker_wallet = Thread_get_wallet_data('USDT')
        self.worker_wallet.finished_labels.connect(self.update_labels_widget)
        self.worker_wallet.start()

        # '현재 잔고 조회' 버튼 클릭 시 동작 정의
        self.pushButton_Initialize.clicked.connect(self.pushButton_Initialize_clicked)


    def thread_runner_table(self):
        self.worker_table_row_01 = Thread_get_hts_data('bithumb', "BTC", 0)
        self.worker_table_row_01.finished_table_row.connect(self.update_table_row_widget)
        self.worker_table_row_01.start()
        self.worker_table_row_02 = Thread_get_hts_data('bithumb', "ETH", 1)
        self.worker_table_row_02.finished_table_row.connect(self.update_table_row_widget)
        self.worker_table_row_02.start()
        self.worker_table_row_03 = Thread_get_hts_data('bithumb', "BCH", 2)
        self.worker_table_row_03.finished_table_row.connect(self.update_table_row_widget)
        self.worker_table_row_03.start()
        self.worker_table_row_03.start()
        self.worker_table_row_04 = Thread_get_hts_data('bithumb', "ETC", 3)
        self.worker_table_row_04.finished_table_row.connect(self.update_table_row_widget)
        self.worker_table_row_04.start()
        self.worker_table_row_05 = Thread_get_hts_data('bithumb', "GALA", 4)
        self.worker_table_row_05.finished_table_row.connect(self.update_table_row_widget)
        self.worker_table_row_05.start()


    def pushButton_Initialize_clicked(self):
        print("초기화 버튼(pushButton_Initialize) 클릭")

        self.label_BalanceSpot.setText(str(0))
        self.label_BalanceFuture.setText(str(0))
        self.label_BalanceTotal.setText(str(0))
        self.label_TimeStamp.setText('0')
        # binance_test.read_wallet_history()

        return 0

    def update_table_row_widget(self, list):
        try:
            self.tableWidget.setItem(list[0], 0, QTableWidgetItem(str(list[1])))
            self.tableWidget.setItem(list[0], 1, QTableWidgetItem(str(list[2])))
            self.tableWidget.setItem(list[0], 2, QTableWidgetItem(str(list[3])))
            self.tableWidget.setItem(list[0], 3, QTableWidgetItem(str(list[4])))
            self.tableWidget.setItem(list[0], 4, QTableWidgetItem(str(list[5])))
            self.tableWidget.setItem(list[0], 5, QTableWidgetItem(str(list[6])))
        except:
            print('wtf')
            pass

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

    def update_labels_widget(self, data):
        try:
            balance_future = 0
            balance_spot = 0
            for key, val in data.items():
                if key == 'balance_spot':
                    balance_spot = val
                    self.label_BalanceSpot.setText(str(balance_spot))

                elif key == 'balance_future':
                    balance_future = val
                    self.label_BalanceFuture.setText(str(val))

            self.label_BalanceTotal.setText(str(balance_spot + balance_future))
            self.label_TimeStamp.setText(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

            global api_parse_cnt_binance, api_parse_cnt_bithumb
            self.label_api_cnt_binance.setText(str(api_parse_cnt_binance))
            self.label_api_cnt_bithumb.setText(str(api_parse_cnt_bithumb))


        except:
            print('wtf3')
            pass

# HTS, ticker 에 따라 해당 정보 가져오는 thread 설계
class Thread_get_hts_data(QThread):

    finished_table_row = pyqtSignal(list)

    def __init__(self, hts, ticker, row):
        super().__init__()
        self.hts = hts
        self.ticker = ticker
        self.row = row
        self.mutex = QMutex()

    def run(self):

        self.hts_instance = BithumbAPI()

        while True:

            time_init = datetime.now()

            global api_parse_cnt_bithumb
            current_price = self.hts_instance.parse_current_price(self.ticker)
            self.mutex.lock()
            api_parse_cnt_bithumb = api_parse_cnt_bithumb + 1
            self.mutex.unlock()

            ohlcv = self.hts_instance.parse_ohlcv(self.ticker, "KRW", "day")
            self.mutex.lock()
            api_parse_cnt_bithumb = api_parse_cnt_bithumb + 1
            self.mutex.unlock()

            last_ma_n, state = self.get_ma_state(current_price, ohlcv, criteria = 'close', n = 5)

            time_end = datetime.now()
            duration = time_end - time_init

            self.finished_table_row.emit([self.row, self.ticker, current_price, last_ma_n, state, duration.microseconds/1000000, time_end])
            self.msleep(500)


            # data_table[self.ticker] = self.get_market_infos_bithumb(self.ticker)
            # self.finished_table.emit(data_table)



    # ohlcv 중 기준값(criteria)에 따른 n일 이평선과 상승장/하락장 판별결과 return함수
    def get_ma_state(self, current_price, ohlcv, criteria, n):
        try:
            ma = ohlcv['close'].rolling(window=5).mean()

            last_ma = ma[-2]

            state = None
            if current_price > last_ma:
                state = "상승장"
            else:
                state = "하락장"

            return last_ma, state
        except:
            print('wtf2')
            return None, None


class Thread_get_wallet_data(QThread):

    finished_labels = pyqtSignal(dict)

    def __init__(self, asset):
        super().__init__()
        self.asset = asset
        self.mutex = QMutex()

    def run(self):

        self.binance_test = BinanceAPI()

        while True:
            data_labels = {}

            data_labels['balance_spot'] = self.binance_test.read_wallet_spot()[self.asset]['total']
            global api_parse_cnt_binance
            self.mutex.lock()
            api_parse_cnt_binance = api_parse_cnt_binance + 1
            self.mutex.unlock()

            data_labels['balance_future'] = self.binance_test.read_wallet_future()[self.asset]['total']
            self.mutex.lock()
            api_parse_cnt_binance = api_parse_cnt_binance + 1
            self.mutex.unlock()

            self.finished_labels.emit(data_labels)
            self.msleep(500)

