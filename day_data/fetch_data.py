import sys, os
from concurrent.futures.thread import ThreadPoolExecutor
import tushare as ts
from sqlalchemy import create_engine
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

ts.set_token('9c4af04257e55b3f490d14ac46c00cd71383ed0846d8e10694907926')
pro = ts.pro_api()

"""
历史行情数据，保存到mysql
"""

startDate = '20150101'
endDate = time.strftime('%Y%m%d', time.localtime(time.time()))

database = 'mysql+pymysql://root:hefei168lj@localhost/'
engineList = []
engine = create_engine(database + 'malason_data' + '?charset=utf8')

for i in range(12):
    engineList.append(create_engine(database + 'malason_data_' + str(i + 1) + '?charset=utf8'))


def fetch_trade_cal():
    trade_cal = pro.trade_cal(exchange='', start_date=startDate, end_date=endDate)
    trade_cal.to_sql('m_fd_data_trade_cal', engine, if_exists='replace')


def fetch_stock():
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    data.to_sql('m_fd_data_cn_stock_list', engine, if_exists='replace')


def fetch_task(index, symbol):
    engine_index = index % 12;
    for _ in range(3):
        try:
            df = ts.pro_bar(pro_api=pro, ts_code=symbol, adj='qfq', start_date=startDate, end_date=endDate)
            df.to_sql('m_fd_data_' + symbol, engineList[engine_index], index=False, if_exists='replace')
        except:
            time.sleep(2)
        else:
            print("fetch data meet exception, the stock is " + symbol)


def batch_fetch_data():
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    with ThreadPoolExecutor(20) as execute:
        for index, symbol in enumerate(data['ts_code']):
            execute.submit(fetch_task, index, symbol)


fetch_trade_cal()
fetch_stock()
batch_fetch_data()

# mysql数据库内不要超过300张表，采用一致性hash算法，将3600个表分到12个库里，每个库最多300张表
# 没有复权的股票，insert改为replace，根据复权因子判断在时间范围内是否存在复权
