from src.visualizers.dashboard import *

tickers = ["BTC", "ETH", "BCH", "ETC"]

def run_dashboard():
    # Window_Dashboard 관련 동작
    app = QApplication(sys.argv)    # QApplication 객체 생성
    window = Dashboard()
    window.show()
    app.exec_()


if __name__ == '__main__':
    print('Program Started...')

    run_dashboard()      # Dashboard 관련 동작




    # Bithumb = BithumbAPI()             # 클래스 생성
    # Bithumb.parse_detail()
    # Bithumb.parse_all()
    # market_classifier()
    # bull_operator()
    # BithumbParser()       # Bithumb 정보 가져오기


    # binance_api = BinanceAPI()
    # binance_api.generating_ohlcv_files(retry_cnt=1, root_dir='.\\data\\Binance_2105062146', quote='BTC')


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







# 엘리어트 파동이론
# 볼륨
# 추세
# 지지
# 저항
# 패턴
# 피보나치
# RSI  - 과매수 과매도 지표
# 다이버전스
# 이평선
# 캔들


#
# 매매법
#  차트분석 통해서 매수 이유를 명확히 찾기
#  - 손절가 / 목표가 같이 설정해서 매매
#
# 손익비 생각
#  -
#
# 최대한 좋은 자리 기다려야 함
#  - 애매하면 절대 매매 하면 안됨
#

