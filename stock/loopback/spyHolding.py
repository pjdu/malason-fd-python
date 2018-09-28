# 基础库导入

from __future__ import division
from __future__ import print_function

import json
import warnings
import time
from multiprocessing import Pool

import abupy
from abupy.MarketBu import ABuDataCache

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import numpy as np
import platform
import pandas as pd
from terminaltables import AsciiTable

import os
import sys


# 获取目录下所有文件名
def get_file_fist(dir, ex_type):
    if not os.path.isdir(dir):
        raise Exception("dir不是文件目录")

    file_list = []
    for file in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, file)) and file.startswith(ex_type):
            file_list.append(file)

    return file_list


def get_system_version():
    sys_str = platform.system()
    if sys_str == "Windows":
        data_source = "C:\\Users\\dell\\abu\\data\\csv"
    else:
        data_source = "/root/abu/data/csv"

    return data_source


def calc_change(a, b):
    return str(round((b - a) / a * 100, 2))


def update_data(symbol):
    current_time_format_1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    current_time_format_2 = time.strftime('%Y%m%d', time.localtime(time.time()))

    abupy.env.g_market_source = abupy.EMarketSourceType.E_MARKET_SOURCE_nt
    abupy.env.g_data_cache_type = abupy.EDataCacheType.E_DATA_CACHE_CSV

    df = abupy.ABuSymbolPd.make_kl_df(symbol, n_folds=None, start='2012-01-01', end=current_time_format_1)
    ABuDataCache.save_kline_df(df, symbol, '20120101', current_time_format_2)

    return df


data_dir = get_system_version()
stock_list = get_file_fist(data_dir, 'us')


def calc_stock_df(symbol):
    stock_file_name = ""
    stock_symbol = symbol[0]
    for stock in stock_list:
        if stock.startswith('us' + stock_symbol + "_"):
            stock_file_name = stock
            break

    if not stock_file_name:
        symbol_stock = abupy.ABuSymbol.code_to_symbol(symbol[0])
        df = update_data(symbol_stock)
    else:
        f = open(os.path.join(data_dir, stock_file_name))
        df = pd.read_csv(f, index_col=0)

    if df is None:
        print(symbol)
        return

    if len(sys.argv) == 3:
        df = df[sys.argv[1]:sys.argv[2]]
        start_price = df.iloc[0]['pre_close']
        end_price = df.iloc[-1]['close']
        return pd.DataFrame(
            {'symbol': [stock_symbol], "name": [symbol[1]], 'p_change': [calc_change(start_price, end_price)]})
    else:
        df['range'] = df.apply(lambda row: calc_change(row['low'], row['high']), axis=1)
        df['symbol'] = stock_symbol
        df['name'] = symbol[1]
        return df.tail(1)[
            ['date', 'symbol', 'name', 'p_change', 'range', 'pre_close', 'open', 'close', 'volume', 'high', 'low']]


with open("./spy.json", "r") as load_f:
    stock_symbols = json.load(load_f)

data = []

pool = Pool(20)
data = pool.map(calc_stock_df, stock_symbols)
pool.close()
pool.join()

df = pd.concat(data)
df.sort_values("p_change", ascending=False, inplace=True)
df['p_change'] = df.apply(lambda row: round(row['p_change'], 2), axis=1)

head = list(df)
nr = df.values.tolist()
c = np.vstack((head, nr)).tolist()
table = AsciiTable(c)
print(table.table)
