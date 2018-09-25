import abupy
import scipy.stats as scs
import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import platform
from abupy.MarketBu import ABuSymbolPd
import os


def calc_change(a, b):
    return (b - a) / a * 100


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


stock_symbol = 'QQQ'
ex_type = 'us'
data_dir = get_system_version()
stock_list = get_file_fist(data_dir, ex_type)

stock_file_name = ""
for stock in stock_list:
    if stock.startswith(ex_type + stock_symbol + "_"):
        stock_file_name = stock
        break

f = open(os.path.join(data_dir, stock_file_name))
df = pd.read_csv(f, index_col=0)

# df = ABuSymbolPd.make_kl_df(stock_symbol, n_folds=5)
df['range'] = df.apply(lambda row: calc_change(row['low'], row['high']), axis=1)

stock_day_change = df.range.values
stock_mean = stock_day_change.mean()
stock_std = stock_day_change.std()

plt.hist(stock_day_change, bins=100, normed=True)
fit_linespace = np.linspace(stock_day_change.min(), stock_day_change.max())
pdf = scs.norm(stock_mean, stock_std).pdf(fit_linespace)
plt.plot(fit_linespace, pdf, lw=2, c='r')

plt.show()
