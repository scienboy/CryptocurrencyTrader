from PyQt5.QtWidgets import *
from PyQt5 import uic


class dashboard_dbgenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/dashboard-dbgenerator2.ui", self)

        print('haha')

        self.pushButton_parse.clicked.connect(self.pushButton_parse_clicked)
        pass

    def pushButton_parse_clicked(self):
        symbol = self.lineEdit.text()
        print('parse_clicked!')

        pass



    def append_each_symbol(self, symbol, timeframe):
        gap_yn = 'y'        # DB에 저장된 가장 최근 데이터와 api로 조회해 온 가장 오래된 데이터 사이 갭이 존재하는지 체크
        print('hahahahahah')
        return gap_yn
        pass

    def check_db_most_recent_time(self, symbol, timeframe):
        pass

    def parse_market_data(self, symbol, timeframe):
        pass

    def check_gap_between_db_api(self, symbol, timeframe, db_recent_time, api_oldest_time):
        pass

