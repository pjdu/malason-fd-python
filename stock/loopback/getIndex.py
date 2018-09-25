import os
import platform
import sys

import pandas as pd
from terminaltables import AsciiTable

symbols_us = [['QQQ', '纳指100'], ['SPY', '标普500'], ['VTI', '大盘指数'], ['FDN', '网络股指数'],
              ['IWM', '美国小盘ETF'], ['IWO', '美国小盘成长'], ['SOXX', '费城半导体指数'],
              ['PGJ', '中概股ETF'], ['XLV', '医疗业ETF'], ['IBB', '生物科技指数'], ['XLF', '金融股指'],
              ['KBE', '银行指数'], ['KRE', '区域银行指数'], ['XLP', '必需消费品指数'],
              ['XLY', '可选消费品指数'], ['VNQ', '不动产信托指数'], ['XLU', '公共事业指数'],
              ['XLI', '工业股指'], ['XLB', '原材料股指'], ['XLE', '能源股指']]

symbols_energy = [['DBO', '原油基金'], ['UNG', '天然气基金'], ['IAU', '黄金ETF'], ['SLV', '白银ETF']]

symbols_global = [['ASGR', '沪深300'], ['EEM', '新兴市场'], ['EFA', '欧洲澳洲远东综合ETF']]


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
    return round((b - a) / a * 100, 2)


def cal_stock_change(stock_symbol):
    for stock in stock_list:
        if stock.startswith(ex_type + stock_symbol + "_"):
            stock_file_name = stock
            break

    f = open(os.path.join(data_dir, stock_file_name))
    try:
        df = pd.read_csv(f, index_col=0)[start_time:end_time]
    except Exception as e:
        print("读取csv文件异常" + stock_symbol)
        return ""

    if not any(df):
        print(stock_symbol)
        return ""
    elif df.empty:
        return ""
    else:
        try:
            start_price = df.iloc[0]['pre_close']
            end_price = df.iloc[-1]['close']
            return calc_change(start_price, end_price)
        except Exception as e:
            print(stock_symbol)
            # print(e)
            return ""


def cal_stock_rank(symbols):
    for symbol in symbols:
        symbol.append(cal_stock_change(symbol[0]))


ex_type = sys.argv[1]
start_time = sys.argv[2]
end_time = sys.argv[3]
sort_type = float(sys.argv[4])

data_dir = get_system_version()
stock_list = get_file_fist(data_dir, ex_type)
if ex_type == 'us':
    cal_stock_rank(symbols_us)
elif ex_type == 'eg':
    cal_stock_rank(symbols_energy)
elif ex_type == 'gl':
    cal_stock_rank(symbols_global)

symbols_us.insert(0, ['symbol', 'name', 'range'])
table = AsciiTable(symbols_us)
print(table.table)
