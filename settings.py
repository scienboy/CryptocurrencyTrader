# settings.py

def init():
    global myList
    myList = {
        "api_parse_cnt_bithumb": 0,     # api_parse_cnt 산출을 위한 전역변수 셋업
        "api_parse_cnt_binance": 0,
        "hts_wallet": 'bithumb',
        "hts_market": 'bithumb',        # (bithumb/binance) bithumb일 경우 KRW, binance는 USDT
        "hts_market_currency": 'KRW',   # (KRW/USDT)        bithumb일 경우 KRW, binance는 USDT
        "mode": 'thread'                # single / thread
    }