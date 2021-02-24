import pybithumb
import openpyxl
import os

class BithumbParser():
    def __init__(self):
        interval_list = ['24h', '12h', '6h', '1h', '30m', '10m', '5m', '3m', '1m']
        tickers = pybithumb.get_tickers()
        if tickers != None:
            print(tickers)
            for ticker in tickers:
                try:
                    if ticker == "CON":
                        ticker = "CON_"
                        os.mkdir('./data/' + str(ticker))
                    else:
                        os.mkdir('./data/' + str(ticker))
                except:
                    print("Folder is exist!")

                retry_cnt = 1
                for interval in interval_list:
                    self.get_candlestick(ticker, interval, retry_cnt)
        else:
            print("Bithumb API Error : Cannot fetch tickers")

    def get_candlestick(self, ticker, interval, retry_cnt):
        try:
            if os.path.isfile("data/" + str(ticker) + "/" + str(ticker) + "_candlestick_" + str(interval) + ".xlsx"):
                print("data/" + str(ticker) + "/" + str(ticker) + "_candlestick_" + str(interval) + ".xlsx - is exist!!")
            else:
                pybithumb.get_candlestick(ticker, "KRW", interval).to_excel("data/" + str(ticker) + "/" + str(ticker) + "_candlestick_" + str(interval) + ".xlsx")
        except:
            print("Retry " + str(retry_cnt) + " of " + str(ticker) + "_candlestick_" + str(interval))
            retry_cnt = retry_cnt + 1
            if retry_cnt < 300:
                self.get_candlestick(ticker, interval, retry_cnt)
            else:
                print("Parsing skipped... " + str(retry_cnt) + " of " + str(ticker) + "_candlestick_" + str(interval))

