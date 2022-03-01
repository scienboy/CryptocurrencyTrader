from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QThread
from src.hts_apis.binance import *
from src.dbs.db_manager import *


class store_market_data(QThread):
# class store_market_data():

    def __init__(self, parent, hts_name='Binance', market='Spot', symbols=['BTC/USDT'], timeframes=['1m']):
        super().__init__()
        self.parent = parent


        self.market = market
        self.hts_name = hts_name
        self.symbols = symbols
        self.timeframes = timeframes
        self.flag_finish = False
        if self.hts_name == 'Binance':
            self.binance_api = BinanceAPI(market=self.market.lower())

    def run(self):

        db_manager = DB_Manager('ohlcv_test7')

        while self.flag_finish == False:

            idx = 0
            # self.timeframes = self.binance_api.timeframes  # 모든 ticker를 기준으로 조회하고자 할 때
            self.symbols = self.binance_api.get_tickers()



            for symbol in self.symbols:

                if symbol.split("/")[1] != "USDT":
                    continue  # 거래기준이 USDT가 아닌 마켓은 조회하지 않음

                for timeframe in self.timeframes:
                    print('start')
                    time_init = datetime.now()  # duration 계산용 timestamp
                    data_time_gap = 0
                    table_name = self.hts_name + '_' +  self.market + '_' + str(symbol.replace('/', '_')) + '_' + str(timeframe)  # sql 입력을 위해 '/' 텍스트 삭제

                    print('1')
                    df_ohlcvs = self.binance_api.get_ohlcvs(symbol, timeframe)
                    print('2')
                    dt_hts_first = datetime.strptime(str(df_ohlcvs['datetime'].min()), '%Y-%m-%d %H:%M:%S')
                    dt_hts_last = datetime.strptime(str(df_ohlcvs['datetime'].max()), '%Y-%m-%d %H:%M:%S')
                    print('3')
                    if self.binance_api.asis_binance_validity(dt_hts_last) == False:
                        continue  # 바이낸스에 오래된(archive) 데이터만 있는 경우 조회하지 않음. ex) 예전엔 있었으나 상장폐지된 코인

                    print('생성자 직전')

                    try:
                        print('initpoint ' + str(idx))
                        dt_db_border = db_manager.parse_dt_border(table_name)  # db 내 가장 신구 데이터 기준시점 조회
                        print('initpoint1')
                        if dt_db_border != False:  # DB 데이터 조회 실패하지 않았다면,
                            dt_db_first = datetime.strptime(dt_db_border['first'], '%Y-%m-%d %H:%M:%S')
                            dt_db_last = datetime.strptime(dt_db_border['last'], '%Y-%m-%d %H:%M:%S')
                            print('initpoint2')
                            if db_manager.asis_db_validity(dt_db_last, timeframe) != False:

                                print('initpoint3')
                                data_time_gap = dt_hts_first - dt_db_last

                                if dt_hts_first <= dt_db_last:  # 신규 데이터와 기존 데이터 사이 time gap 없을 경우
                                    remove_data = df_ohlcvs[df_ohlcvs['datetime'] <= dt_db_last].index
                                    df_ohlcvs_droped = df_ohlcvs.drop(remove_data)

                                    print('initpoint41')
                                    db_manager.insert_data(table_name, df_ohlcvs_droped)
                                    print('initpoint42')

                                else:  # 신규데이터와 기존 데이터 사이의 time gap 존재할 경우

                                    print('initpoint51')
                                    db_manager.insert_data(table_name, df_ohlcvs)

                                    print('initpoint52')
                                    print(str(table_name), ' 데이터 gap이 존재합니다! -> gap = ', str(data_time_gap))
                                    self.label_timegap_val.setText(str(data_time_gap))

                        else:  # DB 데이터 조회 실패시에는 신규 테이블 생성을 시도해보고, 무조건 데이터 다 넣음

                            # 신규 테이블 생성을 위한 변수
                            dict_fields = {
                                'datetime': 'text',
                                'open': 'real',
                                'high': 'real',
                                'low': 'real',
                                'close': 'real',
                                'volume': 'real'
                            }
                            print('initpoint6')

                            db_manager.create_table(table_name, dict_fields)
                            db_manager.insert_data(table_name, df_ohlcvs)

                            print('initpoint7')

                        # 검산작업 추가 필요
                            # output text 예: 데이터 문제없이 들어갔습니다.
                            # or 중복 n건 or 데이터 공백 언제부터 언제까지

                        # timestampp = time.mktime(datetimeobj.timetuple())

                        time_duration = datetime.now() - time_init
                        self.parent.textBrowser.append(str(idx) + table_name)
                        print(idx, table_name)
                        # time_duration = datetime.fromtimestamp(time_duration / 1000).strftime('%Y-%m-%d %H:%M:%S')

                    except:
                        print('problem!! ' + str(idx))
                        del db_manager
                    print('out point ' + str(idx))
                    idx = idx + 1
                    # self.msleep(500)
                    print('finished')

                    if self.flag_finish == True:
                        break

                if self.flag_finish == True:
                    break
        del db_manager

    def finish(self):
        self.flag_finish = True


    def pushButton_parse_clicked(self):

        # db_manager = DB_Manager('ohlcv_test5')

        while self.flag_finish == False:

            idx = 0
            # self.timeframes = self.binance_api.timeframes  # 모든 ticker를 기준으로 조회하고자 할 때
            self.symbols = self.binance_api.get_tickers()

            for symbol in self.symbols:

                if symbol.split("/")[1] != "USDT":
                    continue  # 거래기준이 USDT가 아닌 마켓은 조회하지 않음

                for timeframe in self.timeframes:
                    print('start')
                    time_init = datetime.now()  # duration 계산용 timestamp
                    data_time_gap = 0
                    table_name = self.hts_name + '_' +  self.market + '_' + str(symbol.replace('/', '_')) + '_' + str(timeframe)  # sql 입력을 위해 '/' 텍스트 삭제

                    print('1')
                    df_ohlcvs = self.binance_api.get_ohlcvs(symbol, timeframe)
                    print('2')
                    dt_hts_first = datetime.strptime(str(df_ohlcvs['datetime'].min()), '%Y-%m-%d %H:%M:%S')
                    dt_hts_last = datetime.strptime(str(df_ohlcvs['datetime'].max()), '%Y-%m-%d %H:%M:%S')
                    print('3')
                    if self.binance_api.asis_binance_validity(dt_hts_last) == False:
                        continue  # 바이낸스에 오래된(archive) 데이터만 있는 경우 조회하지 않음. ex) 예전엔 있었으나 상장폐지된 코인

                    print('생성자 직전')
                    db_manager = DB_Manager('ohlcv_test5')

                    try:
                        print('initpoint ' + str(idx))
                        dt_db_border = db_manager.parse_dt_border(table_name)  # db 내 가장 신구 데이터 기준시점 조회
                        print('initpoint1')
                        if dt_db_border != False:  # DB 데이터 조회 실패하지 않았다면,
                            dt_db_first = datetime.strptime(dt_db_border['first'], '%Y-%m-%d %H:%M:%S')
                            dt_db_last = datetime.strptime(dt_db_border['last'], '%Y-%m-%d %H:%M:%S')
                            print('initpoint2')
                            if db_manager.asis_db_validity(dt_db_last, timeframe) != False:

                                print('initpoint3')
                                data_time_gap = dt_hts_first - dt_db_last

                                if dt_hts_first <= dt_db_last:  # 신규 데이터와 기존 데이터 사이 time gap 없을 경우
                                    remove_data = df_ohlcvs[df_ohlcvs['datetime'] <= dt_db_last].index
                                    df_ohlcvs_droped = df_ohlcvs.drop(remove_data)

                                    print('initpoint41')
                                    db_manager.insert_data(table_name, df_ohlcvs_droped)
                                    print('initpoint42')

                                else:  # 신규데이터와 기존 데이터 사이의 time gap 존재할 경우

                                    print('initpoint51')
                                    db_manager.insert_data(table_name, df_ohlcvs)

                                    print('initpoint52')
                                    print(str(table_name), ' 데이터 gap이 존재합니다! -> gap = ', str(data_time_gap))
                                    self.label_timegap_val.setText(str(data_time_gap))

                        else:  # DB 데이터 조회 실패시에는 신규 테이블 생성을 시도해보고, 무조건 데이터 다 넣음

                            # 신규 테이블 생성을 위한 변수
                            dict_fields = {
                                'datetime': 'text',
                                'open': 'real',
                                'high': 'real',
                                'low': 'real',
                                'close': 'real',
                                'volume': 'real'
                            }
                            print('initpoint6')

                            db_manager.create_table(table_name, dict_fields)
                            db_manager.insert_data(table_name, df_ohlcvs)

                            print('initpoint7')

                        # 검산작업 추가 필요
                            # output text 예: 데이터 문제없이 들어갔습니다.
                            # or 중복 n건 or 데이터 공백 언제부터 언제까지

                        # timestampp = time.mktime(datetimeobj.timetuple())

                        time_duration = datetime.now() - time_init
                        self.parent.textBrowser.append(str(idx) + table_name)
                        print(idx, table_name)
                        # time_duration = datetime.fromtimestamp(time_duration / 1000).strftime('%Y-%m-%d %H:%M:%S')

                    except:
                        print('problem!! ' + str(idx))
                        del db_manager
                    print('out point ' + str(idx))
                    idx = idx + 1
                    del db_manager
                    # self.msleep(500)
                    print('finished')

                    if self.flag_finish == True:
                        break

                if self.flag_finish == True:
                    break
        # del db_manager