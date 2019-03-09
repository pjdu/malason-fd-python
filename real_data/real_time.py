import sys, os
import tushare as ts
from common.print import print_df

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

"""
关注股票，实时数据
"""

df = ts.get_realtime_quotes(['601888', '512010', '601012'])[
    ['code', 'name', 'pre_close', 'open', 'price', 'bid', 'ask', 'volume', 'amount', 'high', 'low', 'date', 'time']]

print_df(df)
