
import ccxt
import pandas as pd
import openpyxl

api_key = ""
secret  = ""


binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

#################################################################
x=1000
itv='15m'

# 데이터 저장
btc = binance.fetch_ohlcv(
    symbol="BTC/USDT",
    timeframe=itv,
    since=None,
    limit=x
)


df1 = pd.DataFrame(btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] = df['datetime'] + 32400000
# print(df, '\n\n')
# df=df.assign(rsi=rsi_binance(itv='15m'))
# # print(df, '\n\n')
df1['datetime'] = pd.to_datetime(df1['datetime'], unit='ms')
df1.set_index('datetime', inplace=True)
# df.to_csv('4h_BTC_OHLCV')

# df = pd.read_excel('4h_BTC_OHLCV')
# print(df)

############################################

# RSI 14일간 주가 변동 추세가 갖고 있는 강도를 백분율로 나타낸 것. 추세가 언제 전환될지 예측해줌
# 70이상을 과매수 구간, 30이하를 과매도 구간
# period는 9, 14, 25, 50 등이 사용됨. 주로 14
# RS는 N일간의 상승 평균폭(=_gain) / N일간의 하락 평균폭(=_loss)
################################################

def rsi_calc(ohlc: pd.DataFrame, period: int = 14):
    ohlc = ohlc[4].astype(float)
    delta = ohlc.diff()
    gains, declines = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    declines[declines > 0] = 0

    _gain = gains.ewm(com=(period-1), min_periods=period).mean()
    _loss = declines.abs().ewm(com=(period-1), min_periods=period).mean()

    RS = _gain / _loss
    return pd.Series(100-(100/(1+RS)), name="RSI")
def rsi_binance(itv='1h'):
    binance = ccxt.binance()
    ohlcv = binance.fetch_ohlcv(symbol="BTC/USDT", timeframe=itv, limit=x)
    df = pd.DataFrame(ohlcv)
    rsii = list()
    for i in range(x):
        rsi = round(rsi_calc(df, 14).iloc[x-1-i], 2)
        # print(rsi, "111111111111111111111111111111")
        rsii.append(rsi)
    rsii.reverse()          #리스트 역순 배치

    return rsii




# def rsi_binance(itv='1h'):
#     df = pd.read_csv('4h_BTC_OHLCV')
#     df = df.


#################################################################

# 계좌 잔고 출력
# balance = binance.fetch_balance(params={"type": "future"})
# print(balance['USDT'])
#################################################################

# btc = binance.fetch_ticker("BTC/USDT")
# pprint.pprint(btc['high'])
###########################################
#                   주문

# markets = binance.load_markets()
# symbol = "BTC/USDT"
# market = binance.market(symbol)
# leverage = 10
#
# resp = binance.fapiPrivate_post_leverage({
#     'symbol': market['id'],
#     'leverage': leverage
# })
#
# order = binance.create_market_buy_order(
#     symbol="BTC/USDT",
#     amount=0.001
# )
#################################################################################
# # pprint.pprint(order)
# rsi_binance(itv='4h')
df1['rsi (%)']= rsi_binance(itv)        # 데이타 프레임에 리스트 추가
# print(rsi_binance(itv))
# print(df1, '\n')





#################################################################################


close = df1['close']
# for i in range(len(btc)):
#     close.append(btc[i][4])
#
# close_df=pd.DataFrame(close)

# print(close_series)
# print(df1['close'])
ma5 = close.rolling(window=5).mean()
ma10 = close.rolling(window=10).mean().dropna(axis=0)
ma20 = close.rolling(window=20).mean().dropna(axis=0)
ma50 = close.rolling(window=50).mean().dropna(axis=0)

df1['ma5']= ma5
df1['ma10']= ma10
df1['ma20']= ma20
df1['ma50']= ma50
#
# print(df1)
df1.to_excel('./BTC_Data_15m.xlsx', sheet_name='BTC_Data')






print('END')
# # test
# while True:
#     # print("RSI 15분 : " , rsi_binance(itv='15m'))
#     # print("RSI 1시간 : " , rsi_binance(itv='1h'))
#     print("RSI 4시간 : " , rsi_binance(itv='4h'))
#     time.sleep(1)










# binance=ccxt.binance()
# markets= binance.fetch_tickers()
#
# pprint.pprint(markets.keys())
#
# print(type(markets))
#
# ohlcvs = binance.fetch_ohlcv('ETH/BTC')
#
# for ohlc in ohlcvs:
#      print(datetime.fromtimestamp(ohlc[0]/1000).strftime('%Y-%m-%d %H:%M:%S'))
#
# print(len(ohlcvs))