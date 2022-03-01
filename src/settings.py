# settings.py

def initialize():
    global myList
    myList = {
        "api_parse_cnt_bithumb": 0,     # api_parse_cnt 산출을 위한 전역변수 셋업
        "api_parse_cnt_binance": 0,
        "hts_wallet": 'Binance',
        "hts_market": 'Binance',        # (bithumb/binance) bithumb일 경우 KRW, binance는 USDT
        "hts_market_currency": 'USDT',   # (KRW/USDT)        bithumb일 경우 KRW, binance는 USDT
        "mode": 'thread'                # single / thread
    }