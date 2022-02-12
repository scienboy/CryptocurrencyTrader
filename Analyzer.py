import pandas as pd
import glob
from sklearn.preprocessing import normalize
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

import os
import xlrd
import openpyxl


class Analyzer():
    def __init__(self):

        ## Draw analysis graph

        # exchange: Bithumb, Binance
        # interval:
        # # Bithumb: 24h, 12h, 6h, 1h, 30m, 10m, 5m, 3m, 1m
        # # Binance: 1w, 3d, 1d, 12h, 8h, 6h, 4h, 2h, 1h, 30m, 15m, 5m, 3m, 1m
        # type: open, high, low, close, volume / _diff / _fluctrate
        # locator: Y, M, W, D, h, m

        # # correlation analysis
        # dirname = ".\\data\\Binance\\USDT"
        # usdt_coins = os.listdir(dirname)
        # flag = self.correlation_analyzer(root=dirname, l_base=usdt_coins, interval='6h', type='close', data_period=365, stride=1)
        # # interval: 1w, 3d, 1d, 12h, 8h, 6h, 4h, 2h, 1h, 30m, 15m, 5m, 3m, 1m

        pass

    def correlation_analyzer(self, root='Binance', l_base=['ENJ', 'SAND', 'MANA'], interval='1d', type='close', data_period=365, stride=0):
        df_data_corr_tg = pd.DataFrame()
        for base in l_base:
            full_filename_tg = root + '\\' + base + '\\' + base + '_candlestick_' + interval + '_diff_n_fluctrate.csv'
            df_data = pd.read_csv(full_filename_tg)
            column_name = base + '_' + type
            df_data_corr_tg[column_name] = df_data[type]

        if '_' in type:
            df_data_corr_tg = df_data_corr_tg[stride:]

        df_data_corr_tg = df_data_corr_tg.dropna(axis=1)
        tg_base = df_data_corr_tg.columns
        df_data_corr_tg = df_data_corr_tg.transpose()
        movements = df_data_corr_tg.values
        normalized_movements = normalize(movements)
        mergings = linkage(normalized_movements, method='complete')
        normalized_mergings = normalize(mergings)
        plt.figure(figsize=(10, 5))     # 그래프 크기설정
        # 군집화 결과 출력
        dendrogram(
            mergings,
            labels=tg_base,
            leaf_rotation=90.,
            leaf_font_size=8)
        plt.show()



        # DBSCAN 군집화
        db_scan = DBSCAN(eps=0.01, min_samples=3).fit(normalized_mergings)
        normalized_mergings = pd.DataFrame(normalized_mergings)
        normalized_mergings['cluster_res'] = pd.DataFrame(db_scan.labels_)
        normalized_mergings['base'] = pd.DataFrame(tg_base)

        hello = normalized_mergings.sort_values(by=['cluster_res'], axis = 0, ascending=False)

        a = 1
        print(a)

        # 기존 등락율 시계열 데이터와 합치기
        # 클래스 각각 이름 정하기
        # 클래스 각각에 대해 평균등락율 구하기
        # plot





    def calc_subtract_n_fluctrate_single(self, l_key, l_input, stride):
        temp = pd.DataFrame(columns=['time', 'diff', 'fluctrate'])
        for i in range(0, len(l_input) - stride):
            key = l_key[i + stride]
            diff = l_input[i + stride] - l_input[i]
            fluctrate = (l_input[i + stride] - l_input[i]) / l_input[i]
            temp = temp.append({'time': key, 'diff': diff, 'fluctrate': fluctrate}, ignore_index=True)
        return temp

    def calc_subtract_n_fluctrate_ohlcv(self, df_input, stride):
        temp = df_input
        for j in ['open', 'high', 'low', 'close', 'volume']:
            temp[str(j)+'_diff'] = pd.Series(index=temp.index)
            temp[str(j)+'_fluctrate'] = pd.Series(index=temp.index)

        for i in range(0, len(df_input) - stride):
            for j in ['open', 'high', 'low', 'close', 'volume']:
                diff = df_input[j][i + stride] - df_input[j][i]
                fluctrate = (df_input[j][i + stride] - df_input[j][i]) / df_input[j][i]
                temp.loc[[i+stride], [str(j)+'_diff']] = diff
                temp.loc[[i+stride], [str(j)+'_fluctrate']] = fluctrate
        return temp

    def generate_subtract_n_fluctrate_dataset(self, src_root):
        stride = 1
        l_coinname = os.listdir(src_root)

        for coinname_tg in l_coinname:
            dir_tg = src_root + '\\' + coinname_tg
            l_datafile = os.listdir(dir_tg)
            for datafile in l_datafile:
                full_filename_tg_read = os.path.join(dir_tg, datafile)
                ext = os.path.splitext(full_filename_tg_read)[-1]
                if ext == '.xlsx':
                    df_data_tg = pd.read_excel(full_filename_tg_read, sheet_name = 'Sheet1')
                    full_filename_tg_write = full_filename_tg_read.replace('.xlsx', '_diff_n_fluctrate.csv')
                    if os.path.isfile(full_filename_tg_write):
                        print(full_filename_tg_write + '  file is already exist!!!!!!!!')
                        pass
                    else:
                        df_subtract_n_fluctrate_btc_1d_ohlcv = self.calc_subtract_n_fluctrate_ohlcv(df_data_tg, stride)
                        df_subtract_n_fluctrate_btc_1d_ohlcv.to_csv(full_filename_tg_write)
                        print(full_filename_tg_write + '  file writing is finished')
                else:
                    pass