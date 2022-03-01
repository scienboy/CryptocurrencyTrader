from src.threads.get_market_data import *
from src.threads.get_wallet_data import *
from src.threads.store_market_data import *
from src.visualizers.dashboard_dbgenerator import *

from datetime import *

import src.settings

# form_class_old = uic.loadUiType("ui/1stDesign.ui")[0]
# form_class_bull = uic.loadUiType("ui/bull.ui")[0]

class Dashboard(QMainWindow, uic.loadUiType("../ui/dashboard.ui")[0]):
    def __init__(self):

        src.settings.initialize()   # api_parse_cnt 산출을 위한 전역변수 초기화

        super().__init__()
        self.setupUi(self)

        # self.worker_store_ohlcv = store_market_data(self, hts_name='Binance')     # pushButton(Real-time ohlcv DB generation) 클릭 시 동작하는 DB저장관련 클래스 인스턴스 선언
        self.table_threads_runner()                                         # symbol별 현재가/장세 조회하여 테이블에 내용 기록

        # 지갑 관련 정보 조회
        self.worker_wallet = Thread_get_wallet_data('USDT')
        self.worker_wallet.finished_labels.connect(self.update_labels_widget)
        self.worker_wallet.start()

        # pushButton 기능 정의
        self.pushButton_Initialize.clicked.connect(self.pushButton_Initialize_clicked)      # '초기화' 버튼 클릭 시 동작 정의
        self.pushButton_dbGenerator.clicked.connect(self.pushButton_dbGenerator_clicked)    # 'DB Generator'버튼 클릭 시 동작

        # self.db_generator = dashboard_dbgenerator()     # 미리 second window 인스턴스를 생성해 두어야 순식간에 사라지지 않음. 만일 함수에 선언을 하게되면, 함수가 끝나자마자 윈도우가 사라져버림. 따라서 순식간에 사라지는것으로 인지.

        self.pushButton_finish.clicked.connect(self.pushButton_finish_clicked)

    def pushButton_finish_clicked(self):
        self.worker_store_ohlcv.finish()


    def pushButton_dbGenerator_clicked(self):
        print('DB generation 시작')
        self.worker_store_ohlcv = store_market_data(self, hts_name='Binance', symbols=['BTC/USDT'], timeframes=['1m'])     # pushButton(Real-time ohlcv DB generation) 클릭 시 동작하는 DB저장관련 클래스 인스턴스 선언
        # self.worker_store_ohlcv.pushButton_parse_clicked()
        self.worker_store_ohlcv.start()
        # self.db_generator.show()
        print('DB generation 종료')


    def table_threads_runner(self):
        hts_market = src.settings.myList['hts_market']
        hts_market_currency = src.settings.myList['hts_market_currency']

        if src.settings.myList['mode'] == 'single':
            self.worker_table_row_01 = Thread_get_market_data(hts_market, hts_market_currency, "BTC", 0)
            self.worker_table_row_01.finished_table_row.connect(self.update_table_row_widget)
            self.worker_table_row_01.start()
        elif src.settings.myList['mode'] == 'thread':
            self.worker_table_row_01 = Thread_get_market_data(hts_market, hts_market_currency, "BTC", 0)
            self.worker_table_row_01.finished_table_row.connect(self.update_table_row_widget)
            self.worker_table_row_01.start()
            self.worker_table_row_02 = Thread_get_market_data(hts_market, hts_market_currency, "ETH", 1)
            self.worker_table_row_02.finished_table_row.connect(self.update_table_row_widget)
            self.worker_table_row_02.start()
            self.worker_table_row_03 = Thread_get_market_data(hts_market, hts_market_currency, "BCH", 2)
            self.worker_table_row_03.finished_table_row.connect(self.update_table_row_widget)
            self.worker_table_row_03.start()
            self.worker_table_row_04 = Thread_get_market_data(hts_market, hts_market_currency, "ETC", 3)
            self.worker_table_row_04.finished_table_row.connect(self.update_table_row_widget)
            self.worker_table_row_04.start()
            self.worker_table_row_05 = Thread_get_market_data(hts_market, hts_market_currency, "GALA", 4)
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
                index = data.items().index(ticker)

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

            self.label_BalanceTotal.setText(str(balance_spot + balance_future))                     # 현재 잔액 합산(선물 + 현물)
            self.label_TimeStamp.setText(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))           # 파싱 기준시간
            self.label_api_cnt_bithumb.setText(str(src.settings.myList['api_parse_cnt_bithumb']))   # 빗썸 api 조회 수
            self.label_api_cnt_binance.setText(str(src.settings.myList['api_parse_cnt_binance']))   # binance api 조회 수

        except:
            print('wtf3')
            pass