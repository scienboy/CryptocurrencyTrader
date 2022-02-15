from PyQt5.QtCore import QMutex
from src.hts_apis.bithumb import *
from src.hts_apis.binance import *

import src.settings

class Thread_get_wallet_data(QThread):

    finished_labels = pyqtSignal(dict)

    def __init__(self, asset):
        super().__init__()
        self.asset = asset
        self.mutex = QMutex()
        self.binance_api = BinanceAPI()

    def run(self):

        while True:
            data_labels = {}

            data_labels['balance_spot'] = self.binance_api.read_wallet_spot()[self.asset]['total']

            self.mutex.lock()
            # api_parse_cnt_binance = api_parse_cnt_binance + 1
            src.settings.myList['api_parse_cnt_binance'] = src.settings.myList['api_parse_cnt_binance'] + 1
            self.mutex.unlock()

            data_labels['balance_future'] = self.binance_api.read_wallet_future()[self.asset]['total']
            self.mutex.lock()
            # api_parse_cnt_binance = api_parse_cnt_binance + 1
            src.settings.myList['api_parse_cnt_binance'] = src.settings.myList['api_parse_cnt_binance'] + 1
            self.mutex.unlock()

            self.finished_labels.emit(data_labels)
            self.msleep(500)

