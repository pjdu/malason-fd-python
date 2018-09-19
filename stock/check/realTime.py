import tushare as ts

df = ts.get_realtime_quotes(['600188', '600763'])

print(df[['code','name','price','bid','ask','volume','amount','time']])