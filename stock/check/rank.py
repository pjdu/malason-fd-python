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
#sys.path.insert(0, os.path.abspath('../'))
import abupy

# 使用实时数据 abupy.env.enable_example_env_ipython()
# abupy.env.disable_example_env_ipython()


def get_system_version():
    sys_str = platform.system()
    if sys_str == "Windows":
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
            file_list.append(file)

    return file_list


def calcChange(a, b):
    return round((b - a) / a * 100, 2)


def quick_sort(myList, start, end):
    # 判断low是否小于high,如果为false,直接返回
    if start < end:
        i, j = start, end
        # 设置基准数
        base = myList[i]

        while i < j:
            # 如果列表后边的数,比基准数大或相等,则前移一位直到有比基准数小的数出现
            while (i < j) and (sort_type * (myList[j][1] - base[1]) <= 0):
                j = j - 1

            # 如找到,则把第j个元素赋值给第个元素i,此时表中i,j个元素相等
            myList[i] = myList[j]

            # 同样的方式比较前半区
            while (i < j) and (sort_type * (myList[i][1] - base[1]) >= 0):
                i = i + 1
            myList[j] = myList[i]
        # 做完第一轮比较之后,列表被分成了两个半区,并且i=j,需要将这个数设置回base
        myList[i] = base

        # 递归前后半区
        quick_sort(myList, start, i - 1)
        quick_sort(myList, j + 1, end)

    return myList


def cal_stock_change(stock):
    rank_info = stock.split('_')
    stock_symbol = rank_info[0]
    stock_symbol = stock_symbol.split('-')[0].split('*')[0].split('+')[0]
    # 缓存数据为abu安装内置数据，支持股票非常少，全量更新cvs文件后，不会更改缓存数据，此时make_kl_df其实是从网络更新数据（一般情况下），此处修改为直接读取cvs文件到df内，速度更快，前复权数据有问题，如合股
    f = open(os.path.join(data_dir, stock))
    try:
        df = pd.read_csv(f, index_col=0)[start_time:end_time]
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
            # print(e)
            return []


# 全市场回测，股票涨幅排名
def cal_stock_rank(ex_type):
    stock_list = get_file_fist(data_dir, ex_type)

    pool = Pool(20)
    rl = pool.map(cal_stock_change, stock_list)
    pool.close()
    pool.join()

    while [] in rl:
        rl.remove([])

    quick_sort(rl, 0, len(rl) - 1)
    print_list = rl[page_begin_num:page_num]

    for print_str in print_list:
        print_str[1] = str(print_str[1]) + "%"

    print_list.insert(0, ['symbol', 'range'])
    table = AsciiTable(print_list)
    print(table.table)
    return rl


ex_type = sys.argv[1]
start_time = sys.argv[2]
end_time = sys.argv[3]
page_begin_num = int(sys.argv[4]) - 1
page_num = int(sys.argv[5])
sort_type = float(sys.argv[6])
data_dir = get_system_version()
cal_stock_rank(ex_type)
