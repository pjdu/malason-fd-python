# -*- coding:UTF-8 -*-
# 基础库导入

from __future__ import division
from __future__ import print_function

import warnings

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import os
import sys
import platform
import pandas as pd

# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy

# 使用沙盒数据，目的是和书中一样的数据环境
abupy.env.enable_example_env_ipython()

from abupy import ABuSymbolPd

# 使用实时数据 abupy.env.enable_example_env_ipython()
abupy.env.disable_example_env_ipython()

sysstr = platform.system()
if(sysstr =="Windows"):
    data_source = "C:\\Users\\dell\\abu\\data\\csv"
else:
    data_source = "/root/abu/data/csv"
ex_type = "us"


# 获取目录下所有文件名
def get_file_fist(dir, ex_type):
    if not os.path.isdir(dir):
        raise Exception("dir不是文件目录")

    file_list = []
    for file in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, file)) and file.startswith(ex_type):
            file_list.append(file)

    return file_list


def calcChange(a, b):
    return round((b - a) / a * 100, 2)

# 全市场回测，股票涨幅排名
def cal_stock_rank(ex_type, start_time, end_time):
    symbols = []
    ranges = []
    sotck_list = get_file_fist(data_source, ex_type)
    for stock in sotck_list:
        rank_info = stock.split('_')
        stock_symbol = rank_info[0]
        df = ABuSymbolPd.make_kl_df(stock_symbol, n_folds=8)[start_time:end_time]
        if not df.empty:
            symbols.append(stock_symbol)
            ranges.append(calcChange(df['close'][0], df['close'][-1]))

    stock_rank = pd.Series(ranges, index=symbols)
    stock_rank.sort_values(ascending=False, inplace=True)

    return stock_rank


stock_rank = cal_stock_rank(sys.argv[1], sys.argv[2], sys.argv[3])
print(stock_rank)