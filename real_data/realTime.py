import tushare as ts

from common import print_df

df = ts.get_realtime_quotes(['601888', '512010', '601012'])[
    ['code', 'name', 'pre_close', 'open', 'price', 'bid', 'ask', 'volume', 'amount', 'high', 'low', 'date', 'time']]

print_df(df)
