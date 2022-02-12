import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
from Analyzer import *
import matplotlib.cbook as cbook
import numpy as np
import datetime

# from varname import nameof


class Analyzer_plot():
    def __init__(self):
        pass

    def draw_time_ohlcv_graph(self, root, l_base=['ENJ', 'SAND'], interval='24h', type='close', data_period='365', locator='D'):  # type: ohlcv, _diff, _fluctrate
        fig, ax = plt.subplots()

        l_data_all = []
        for i in l_base:
            data_tg = root + '\\' + i + '\\' + i + '_candlestick_' + interval + '_diff_n_fluctrate.csv'

            if os.path.isfile(data_tg):
                df_data = pd.read_csv(data_tg)
                l_data_all.append(df_data)
                pass
            else:
                print(data_tg + '  file is not existing!!!!!!!!')
                src_tg = data_tg.replace('_diff_n_fluctrate.csv', '.csv')

                # df_data_tg = pd.read_excel(src_tg, sheet_name='Sheet1')
                df_data_tg = pd.read_csv(src_tg)

                analyzer = Analyzer()
                df_subtract_n_fluctrate_btc_1d_ohlcv = analyzer.calc_subtract_n_fluctrate_ohlcv(df_data_tg, stride=1)
                df_subtract_n_fluctrate_btc_1d_ohlcv.to_csv(data_tg)
                print(data_tg + '  file writing is finished')

                df_data = pd.read_csv(data_tg)
                l_data_all.append(df_data)

            # df_data_tg = pd.read_csv(".\data\BTC\BTC_candlestick_24h_diff_n_fluctrate.csv")
            # df_data_SAND = pd.read_csv(".\data\SAND\SAND_candlestick_24h_24h_diff_n_fluctrate.csv")
            # # df_data_tg = pd.read_csv(".\data\BTC\BTC_candlestick_24h_diff_n_fluctrate.csv")
            # # df_data_tg = pd.read_csv(".\data\BTC\BTC_candlestick_24h_diff_n_fluctrate.csv")


        data_period = -data_period
        idx = 0
        for data in l_data_all:
            ax.plot(pd.to_datetime(data["time"][data_period:]), data[type][data_period:], "-", label=l_base[idx], alpha=.5)
            idx = idx + 1

        # ax.xaxis.set_major_locator(mdates.YearLocator(interval=6))
        if locator == 'Y':
            ax.xaxis.set_major_locator(mdates.YearLocator())
            ax.xaxis.set_minor_locator(mdates.MonthLocator())
        elif locator == 'M':
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
        elif locator == 'W':
            ax.xaxis.set_major_locator(mdates.WeekdayLocator())
            ax.xaxis.set_minor_locator(mdates.DayLocator())
        elif locator == 'D':
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_minor_locator(mdates.HourLocator())
        elif locator == 'h':
            ax.xaxis.set_major_locator(mdates.HourLocator())
            ax.xaxis.set_minor_locator(mdates.MinuteLocator())
        elif locator == 'm':
            ax.xaxis.set_major_locator(mdates.MinuteLocator())
        else:
            print('[Warning] Locator error')
            pass
        # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

        # a = max(data["time"])
        # b = np.datetime64(a, 'M')
        # Round to nearest years.

        datemin = min(data["time"][data_period:])
        datemax = max(data["time"][data_period:])
        # ax.set_xlim([datemin, datemax])
        # ax.set_xlim([datetime.date(2014, 1, 26), datetime.date(2014, 2, 1)])

        # fig.autofmt_xdate()
        ##################################


        plt.grid()
        plt.legend(fontsize=13)
        plt.xticks(rotation=90)
        # plt.xticks(np.arange(min(data["time"][cnt:]), max(data["time"][cnt:]), 10))

        plt.show()
        return '1'
