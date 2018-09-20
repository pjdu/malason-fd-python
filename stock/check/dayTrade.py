# 基础库导入

from __future__ import division
from __future__ import print_function

import warnings

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
    return (b - a) / a * 100


ex_type = sys.argv[1]
stock_symbol = sys.argv[2]
data_dir = get_system_version()
stock_list = get_file_fist(data_dir, ex_type)

for stock in stock_list:
    if stock.startswith(ex_type + stock_symbol + "_"):
        stock_file_name = stock
        break

f = open(os.path.join(data_dir, stock_file_name))
df = pd.read_csv(f, index_col=0)

if len(sys.argv) == 5:
    df = df[sys.argv[3]:sys.argv[4]]

df['range'] = df.apply(lambda row: calc_change(row['low'], row['high']), axis=1)

result = []

head_data = df.tail(1)[['date', 'p_change', 'range', 'pre_close', 'open', 'close', 'volume', 'high', 'low']]
head = list(head_data)
nr = head_data.values.tolist()
c = np.vstack((head, nr)).tolist()
table = AsciiTable(c)
print(table.table)
print('\n')

## print(df.loc[:,['high','low', 'range']])
result.append(["日内平均波动幅度", "%.2f%%" % (df['range'].mean())])

count = df.iloc[:, 0].size
upCount = df[df['close'] > df['pre_close']].iloc[:, 0].size
downCount = df[df['close'] < df['pre_close']].iloc[:, 0].size

result.append(["收涨概率", "%.2f%%" % (upCount / count * 100)])
result.append(["收跌概率", "%.2f%%" % (downCount / count * 100)])

## 高开走势
hdf = df[df['open'] > df['pre_close']]
count = hdf.iloc[:, 0].size
upCount = hdf[hdf['close'] > hdf['open']].iloc[:, 0].size

result.append(["高开高走概率", "%.2f%%" % (upCount / count * 100)])

hdf1 = hdf[hdf['close'] > hdf['open']]
df['range'] = hdf1.apply(lambda row: calc_change(row['open'], row['close']), axis=1)
result.append(["高开高走，收盘平均涨幅", "%.2f%%" % (df['range'].mean())])

df['range'] = hdf1.apply(lambda row: calc_change(row['open'], row['high']), axis=1)
result.append(["高开高走，最大平均涨幅", "%.2f%%" % (df['range'].mean())])

df['range'] = hdf1.apply(lambda row: calc_change(row['open'], row['low']), axis=1)
result.append(["高开高走，最大平均回撤", "%.2f%%" % (df['range'].mean())])

result.append(["高开低走概率", "%.2f%%" % ((count - upCount) / count * 100)])

hdf2 = hdf[hdf['close'] < hdf['open']]
df['range'] = hdf2.apply(lambda row: calc_change(row['open'], row['close']), axis=1)
result.append(["高开低走，收盘平均跌幅", "%.2f%%" % (df['range'].mean())])

df['range'] = hdf2.apply(lambda row: calc_change(row['open'], row['low']), axis=1)
result.append(["高开低走，最大平均跌幅", "%.2f%%" % (df['range'].mean())])

df['range'] = hdf2.apply(lambda row: calc_change(row['open'], row['high']), axis=1)
result.append(["高开低走，最大平均反弹", "%.2f%%" % (df['range'].mean())])

## 低开走势
hdf = df[df['open'] < df['pre_close']]
count = hdf.iloc[:, 0].size
upCount = hdf[hdf['close'] > hdf['open']].iloc[:, 0].size

result.append(["低开高走概率", "%.2f%%" % (upCount / count * 100)])

hdf1 = hdf[hdf['close'] > hdf['open']]
df['range'] = hdf1.apply(lambda row: calc_change(row['open'], row['close']), axis=1)
result.append(["低开高走，收盘平均涨幅", "%.2f%%" % (df['range'].mean())])

df['range'] = hdf1.apply(lambda row: calc_change(row['open'], row['high']), axis=1)
result.append(["低开高走，最大平均涨幅", "%.2f%%" % (df['range'].mean())])

df['range'] = hdf1.apply(lambda row: calc_change(row['open'], row['low']), axis=1)
result.append(["低开高走，最大平均回撤", "%.2f%%" % (df['range'].mean())])

result.append(["低开低走概率", "%.2f%%" % ((count - upCount) / count * 100)])

hdf2 = hdf[hdf['close'] < hdf['open']]
df['range'] = hdf2.apply(lambda row: calc_change(row['open'], row['close']), axis=1)
result.append(["低开低走，收盘平均跌幅", "%.2f%%" % (df['range'].mean())])

df['range'] = hdf2.apply(lambda row: calc_change(row['open'], row['low']), axis=1)
result.append(["低开低走，最大平均跌幅", "%.2f%%" % (df['range'].mean())])

df['range'] = hdf2.apply(lambda row: calc_change(row['open'], row['high']), axis=1)
result.append(["低开低走，最大平均反弹", "%.2f%%" % (df['range'].mean())])

table = AsciiTable(result)
print(table.table)
