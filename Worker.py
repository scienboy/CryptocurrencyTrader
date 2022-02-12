from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Worker import *
from Calculator import *
import pykorbit

import time
import datetime


class Worker(QThread):

    customized_signal_fill_table = pyqtSignal(dict)

    def __init__(self, tickers):
        super().__init__()
        self.tickers = tickers

    def run(self):
        calculator = Calculator()
        while True:
            data = {}

            for ticker in self.tickers:
                data[ticker] = calculator.get_market_infos(ticker)

            self.customized_signal_fill_table.emit(data)        # emit: 데이터 처리가 완료되었으므로 이벤트를 발생.
            self.msleep(100)

