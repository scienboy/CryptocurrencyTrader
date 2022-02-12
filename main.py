from bithumb_data_parser import *
from Tester import *
from Analyzer import *
from Analyzer_plot import *
from binance_test import *
from bithumb_test import *
from coinmarketcap_api import *
from Window_Dashboard import *

# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    print('Program Started...')

    app = QApplication(sys.argv)          # QApplication 객체 생성

    # # 객체 생성
    # label = QLabel("HelloObj")
    # label.show()

    # # 버튼 객체 생성
    # btn = QPushButton("HelloBtn")
    # btn.show()


    window = Window_Dashboard(tickers)          # 동작안함
    window.show()

    app.exec_()                         # 이벤트 루프 생성


    # Bithumb.parse_detail()
    # Bithumb.parse_all()
    # market_classifier()
    # bull_operator()

    # Bithumb = BithumbAPI()             # 클래스 생성

    # binance_api = BinanceAPI()
    # binance_api.generating_ohlcv_files(retry_cnt=1, root_dir='.\\data\\Binance_2105062146', quote='BTC')

    # BithumbParser()       # Bithumb 정보 가져오기

    # test = Tester()

    # analyzer = Analyzer()
    # analyzer.generate_subtract_n_fluctrate_dataset('.\\data\\Binance\\BTC')           # 변동성 지표 파일 만드는 함수

    # plotter = Analyzer_plot()
    # # flag = plotter.draw_time_ohlcv_graph(root='.\\data\\Binance_2105062146\\BTC', l_base=['MANA', 'LTC', 'ZEN', 'XRP', 'BCH'], interval='1d', type='close', data_period=500, locator='M')
    # flag = plotter.draw_time_ohlcv_graph(root='.\\data\\Binance_2105062146\\BTC', l_base=['BCH', 'LTC', 'ETH', 'QTUM', 'XRP'], interval='1d', type='close_fluctrate', data_period=500, locator='M')

    # CoinmarketcapAPI()
    print('Program Ended...')


# See PyCharm help at https://wWww.jetbrains.com/help/pycharm/

## 해야 할 일들
# 0. 구매하고, 파는 코드 짜보기
# 1. 화면 구현해서 클릭하면 바로 구매하는 프로그램 짜기
# 2. 이력 데이터 쌓아서 보는 프로그램 짜기
# 3. 수수료로 나간 금액도 확인하는 프로그램 짜기
# 4. 저절로 적당히 되는 것은 없다!
# 5. 지금까지 내가 입금한 것 대비 얼마나 땄는지 확인해보자!!!

# 10. 상승으로 튀는 코인 순서 예측하기
# # # 데이터 업데이트
# # # 타겟 데이터 기준 값 읽어오기
# # # 읽어온 데이터 뿌려보기
# # # 읽어온 데이터 기준으로 일별 ohlc 평균값 계산
# # # 이평선 보고 ohlc 평균값으로 구매하는 알고리즘
# # # 그 다음에 얼마 땃는지 확인

