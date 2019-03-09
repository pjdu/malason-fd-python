import sys, os
import tushare as ts
import time
from pyecharts import Line

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

ts.set_token('9c4af04257e55b3f490d14ac46c00cd71383ed0846d8e10694907926')
pro = ts.pro_api()

"""
大盘指数历史走势
"""

startDate = '20150101'
endDate = time.strftime('%Y%m%d', time.localtime(time.time()))

stock_list = [{'ts_code': '399006.SZ', 'ts_name': "创业板指"},
              {'ts_code': '399005.SZ', 'ts_name': "中小板指"},
              {'ts_code': '000037.SH', 'ts_name': "上证医药"},
              {'ts_code': '399004.SZ', 'ts_name': "深证100R"},
              {'ts_code': '510310.SH', 'ts_name': "沪深300"},
              {'ts_code': '399951.SZ', 'ts_name': "300银行"},
              {'ts_code': '000016.SH', 'ts_name': "上证50"},
              {'ts_code': '399919.SZ', 'ts_name': "300价值"},
              {'ts_code': '399952.SZ', 'ts_name': "300地产"}]

line = Line("指数行情", width=1600, height=800)
for stock in stock_list:
    df = pro.index_daily(ts_code=stock['ts_code'], adj='qfq', start_date=startDate, end_date=endDate)
    if df is not None:
        df = df.sort_index(ascending=True)
        line.add(stock['ts_name'], df['trade_date'], df['close'], mark_point=["max", "min"])

line.show_config()
line.render('index_daily.html')
