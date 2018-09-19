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
from multiprocessing import Pool
from terminaltables import AsciiTable

# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy

# 使用实时数据 abupy.env.enable_example_env_ipython()
abupy.env.disable_example_env_ipython()


def get_system_version():
    sysstr = platform.system()
    if (sysstr == "Windows"):
        data_source = "C:\\Users\\dell\\abu\\data\\csv"
    else:
        data_source = "/root/abu/data/csv"

    return data_source


# 获取目录下所有文件名
def get_file_fist(dir, ex_type):
    if not os.path.isdir(dir):
        raise Exception("dir不是文件目录")

    file_list = []
    for file in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, file)) and file.startswith(ex_type):
            file_list.append(os.path.join(dir, file))

    return file_list


def calcChange(a, b):
    return round((b - a) / a * 100, 2)


def cal_stock_change(stock):
    rank_info = stock.split('_')
    stock_symbol = rank_info[0]
    stock_symbol = stock_symbol.split('-')[0].split('*')[0].split('+')[0]
	# 缓存数据为abu安装内置数据，支持股票非常少，全量更新cvs文件后，不会更改缓存数据，此时make_kl_df其实是从网络更新数据（一般情况下），此处修改为直接读取cvs文件到df内，速度更快
    #df = abupy.ABuSymbolPd.make_kl_df(stock_symbol, n_folds=8)[start_time:end_time]
    f = open(stock)
    try:
        df = pd.read_csv(f)
    except Exception as e:
        print("读取csv文件异常" + stock_symbol)
        return []

    if not any(df):
        print(stock_symbol)
        return []
    elif df.empty:
        return []
    else:
        try:
            start_price = df.iloc[0]['pre_close']
            end_price = df.iloc[-1]['close']
            return [stock_symbol, calcChange(start_price, end_price)]
        except Exception as e:
            print(stock_symbol)
            #print(e)
            return []


def list_of_groups(init_list, children_list_len):
    list_of_groups = zip(*(iter(init_list),) * children_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % children_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


# 全市场回测，股票涨幅排名
def cal_stock_rank(ex_type):
    stock_list = get_file_fist(get_system_version(), ex_type)

    pool = Pool(20)
    rl = pool.map(cal_stock_change, stock_list)
    pool.close()
    pool.join()

    #价格排序后打印
    table = AsciiTable(rl)
    print(table.table)
    return rl


ex_type = sys.argv[1]
start_time = sys.argv[2]
end_time = sys.argv[3]

cal_stock_rank(ex_type)
