import sys, os
import tushare as ts
import time
from pyecharts import Line, Page

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

ts.set_token('9c4af04257e55b3f490d14ac46c00cd71383ed0846d8e10694907926')
pro = ts.pro_api()

"""
板块历史走势
"""

startDate = '20100101'
endDate = time.strftime('%Y%m%d', time.localtime(time.time()))

stock_list = [{'ts_code': '601012.SH', 'ts_name': "隆基股份"},
              {'ts_code': '002129.SZ', 'ts_name': "中环股份"},
              {'ts_code': '300274.SZ', 'ts_name': "阳光电源"},
              {'ts_code': '600438.SH', 'ts_name': "通威股份"}]

page = Page()
for stock in stock_list:
    line = Line(stock['ts_name'], width=1600, height=800)
    df = ts.pro_bar(pro_api=pro, ts_code=stock['ts_code'], adj='qfq', start_date=startDate, end_date=endDate)
    if df is not None:
        df = df.sort_index(ascending=True)
        line.add(stock['ts_name'], df['trade_date'], df['close'], mark_point=["max", "min"])
        page.add_chart(line)

page.render('market_daily.html')
