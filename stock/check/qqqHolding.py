# 基础库导入

from __future__ import division
from __future__ import print_function

import warnings

import abupy

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import numpy as np
import platform
import pandas as pd
import abupy
from abupy import ABuSymbolPd, EMarketSourceType
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
    return str(round((b - a) / a * 100, 2)) + "%"


data_dir = get_system_version()
stock_list = get_file_fist(data_dir, 'us')


def calc_stock_df(stock_symbol):
    stock_file_name = ""
    for stock in stock_list:
        if stock.startswith('us' + stock_symbol + "_"):
            stock_file_name = stock
            break

    if not stock_file_name:
        abupy.env.g_market_source = EMarketSourceType.E_MARKET_SOURCE_nt
        df = ABuSymbolPd.make_kl_df(stock_symbol)
    else:
        f = open(os.path.join(data_dir, stock_file_name))
        df = pd.read_csv(f, index_col=0)

    if len(sys.argv) == 3:
        df = df[sys.argv[1]:sys.argv[2]]
        start_price = df.iloc[0]['pre_close']
        end_price = df.iloc[-1]['close']
        return pd.DataFrame({'symbol': [stock_symbol], 'p_change': [calc_change(start_price, end_price)]})
    else:
        df['range'] = df.apply(lambda row: calc_change(row['low'], row['high']), axis=1)
        df['p_change'] = df.apply(lambda row: str(round(row['p_change'], 2)) + "%", axis=1)
        df['symbol'] = stock_symbol

        return df.tail(1)[
            ['date', 'symbol', 'p_change', 'range', 'pre_close', 'open', 'close', 'volume', 'high', 'low']]

stock_symbols = ["QQQ", "AAPL", "AMZN", "MSFT", "GOOG", "FB", "GOOGL", "INTC", "CSCO", "NVDA", "CMCSA"]
data = []
for symbol in stock_symbols:
    data.append(calc_stock_df(symbol))

df = pd.concat(data)

head = list(df)
nr = df.values.tolist()
c = np.vstack((head, nr)).tolist()
table = AsciiTable(c)
print(table.table)
