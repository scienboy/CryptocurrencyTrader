from PyQt5.QtWidgets import *
from PyQt5 import uic

from src.hts_apis.binance import *
from src.dbs.db_manager import *


class dashboard_dbgenerator(QWidget):
    def __init__(self):
        super().__init__()

        print('haha')
        self.ui = uic.loadUi("ui/dashboard-dbgenerator2.ui", self)
        self.binance_api = BinanceAPI()
        self.pushButton_parse.clicked.connect(self.pushButton_parse_clicked)
        self.db_manager = DB_Manager('ohlcv_binance')

    def pushButton_parse_clicked(self):
        # symbol = self.lineEdit_symbol.text()
        # timeframe = self.lineEdit_timeframe.text()

        dict_fields = {
            'datetime' : 'text',
            'open' : 'real',
            'high' : 'real',
            'low' : 'real',
            'close' : 'real',
            'volume' : 'real'
        }

        timeframes = self.binance_api.timeframes
        symbols = self.binance_api.get_tickers()

        idx = 0
        for symbol in symbols:
            if symbol.split("/")[1] != "USDT":
                continue    # 거래기준이 USDT가 아닌 마켓은 조회하지 않음

            for timeframe in timeframes:
                data_time_gap = 0
                time_init = datetime.now()      # duration 계산용 timestamp

                table_name = str(symbol.replace('/', '_')) + '_' + str(timeframe)       # sql 입력을 위해 '/' 텍스트 삭제

                datetime_db_last, datetime_db_first = self.db_manager.parse_dt_border(table_name)

                df_ohlcvs = self.binance_api.get_ohlcvs(symbol, timeframe)
                datetime_binance_first = datetime.strptime(str(df_ohlcvs['datetime'].min()), '%Y-%m-%d %H:%M:%S')
                datetime_binance_last = datetime.strptime(str(df_ohlcvs['datetime'].max()), '%Y-%m-%d %H:%M:%S')

                if self.binance_api.asis_binance_validity(datetime_binance_last) == False:
                    continue        # 바이낸스에 오래된 데이터만 있는 경우 조회하지 않음

                if datetime_db_last != 0:       # DB 데이터 조회 실패하지 않았다면,

                    datetime_db_last = datetime.strptime(datetime_db_last, '%Y-%m-%d %H:%M:%S')
                    datetime_db_first = datetime.strptime(datetime_db_first, '%Y-%m-%d %H:%M:%S')
                    
                    if self.db_manager.asis_db_validity(datetime_db_last, timeframe) == False:
                        continue  # 최신데이터가 DB에 있는 경우에는 api조회를 하지 않음
                        
                    data_time_gap = datetime_binance_first - datetime_db_last

                    if datetime_binance_first <= datetime_db_last:     # 신규 데이터와 기존 데이터 사이 time gap 없을 경우
                        remove_data = df_ohlcvs[df_ohlcvs['datetime'] <= datetime_db_last].index
                        df_ohlcvs_droped = df_ohlcvs.drop(remove_data)
                        self.db_manager.insert_data(table_name, df_ohlcvs_droped)

                    else:   # 신규데이터와 기존 데이터 사이의 time gap 존재할 경우
                        self.db_manager.insert_data(table_name, df_ohlcvs)
                        print(str(table_name), ' 데이터 gap이 존재합니다! -> gap = ', str(data_time_gap))
                        self.label_timegap_val.setText(str(data_time_gap))

                else:   # DB 데이터 조회 실패시에는 무조건 데이터 다 넣음
                    self.db_manager.create_table(table_name, dict_fields)
                    self.db_manager.insert_data(table_name, df_ohlcvs)

                # timestampp = time.mktime(datetimeobj.timetuple())

                time_duration = datetime.now() - time_init
                # time_duration = datetime.fromtimestamp(time_duration / 1000).strftime('%Y-%m-%d %H:%M:%S')


                self.tableWidget.setItem(idx, 0, QTableWidgetItem(table_name))
                self.tableWidget.setItem(idx, 1, QTableWidgetItem(str(datetime_db_first)))
                self.tableWidget.setItem(idx, 2, QTableWidgetItem(str(datetime_db_last)))
                self.tableWidget.setItem(idx, 3, QTableWidgetItem(str(datetime_binance_first)))
                self.tableWidget.setItem(idx, 4, QTableWidgetItem(str(datetime_binance_last)))
                self.tableWidget.setItem(idx, 5, QTableWidgetItem(str(data_time_gap)))
                # self.tableWidget.setItem(idx, 6, QTableWidgetItem(binance_newest_datetime))
                self.tableWidget.setItem(idx, 7, QTableWidgetItem(str(time_duration)))
                print(idx, table_name)
                idx = idx + 1




    # def append_each_symbol(self, symbol, timeframe):
    #     gap_yn = 'y'        # DB에 저장된 가장 최근 데이터와 api로 조회해 온 가장 오래된 데이터 사이 갭이 존재하는지 체크
    #     print('hahahahahah')
    #     return gap_yn
    #     pass
    #
    # def check_db_most_recent_time(self, symbol, timeframe):
    #     pass
    #
    # def parse_market_data(self, symbol, timeframe):
    #     pass
    #
    # def check_gap_between_db_api(self, symbol, timeframe, db_recent_time, api_oldest_time):
    #     pass

