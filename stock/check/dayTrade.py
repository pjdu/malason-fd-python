# 基础库导入

from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from terminaltables import AsciiTable

import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy

# 使用实时数据 abupy.env.enable_example_env_ipython()
abupy.env.disable_example_env_ipython()

from abupy import abu, EMarketTargetType, AbuMetricsBase, ABuMarketDrawing, ABuProgress, ABuSymbolPd, get_price, ABuIndustries
from abupy import EMarketDataFetchMode, EDataCacheType, EMarketSourceType, FuturesBaseMarket, TCBaseMarket, ABuDateUtil
from abupy import AbuDataParseWrap, StockBaseMarket, SupportMixin, ABuNetWork, Symbol, code_to_symbol

# 切换至腾讯数据源，然后进行美股数据全市场更新
# %%time
# abupy.env.g_market_source = EMarketSourceType.E_MARKET_SOURCE_tx
# abupy.env.g_data_cache_type = EDataCacheType.E_DATA_CACHE_CSV
# abu.run_kl_update(start='2015-06-01', end='2018-09-09', market=EMarketTargetType.E_MARKET_TARGET_US, n_jobs=10)

def calcChange(a, b):
    return (b - a)/a * 100

symbol = sys.argv[1]
if len(sys.argv) == 2:
    df = ABuSymbolPd.make_kl_df(symbol, n_folds=8)
else:	
    df = ABuSymbolPd.make_kl_df(symbol, n_folds=8)[sys.argv[2]:sys.argv[3]]
	
df['range'] = df.apply(lambda row: calcChange(row['low'], row['high']), axis=1)

result = []

head_data = df.tail(1)[['date', 'p_change', 'range', 'pre_close', 'open', 'close', 'volume', 'high', 'low']]
head = list(head_data)
nr = head_data.values.tolist()
c=np.vstack((head, nr)).tolist()
table = AsciiTable(c)
print(table.table)
print('\n')

## print(df.loc[:,['high','low', 'range']])
result.append(["日内平均波动幅度", "%.2f%%" %(df['range'].mean())])

count = df.iloc[:,0].size
upCount = df[df['close'] > df['pre_close']].iloc[:,0].size
downCount = df[df['close'] < df['pre_close']].iloc[:,0].size

result.append(["收涨概率",  "%.2f%%" %(upCount/count * 100)])
result.append(["收跌概率",  "%.2f%%" %(downCount/count * 100)])

## 高开走势
hdf = df[df['open'] > df['pre_close']]
count = hdf.iloc[:,0].size
upCount = hdf[hdf['close'] > hdf['open']].iloc[:,0].size

result.append(["高开高走概率",  "%.2f%%" %(upCount/count * 100)])

hdf1 = hdf[hdf['close'] > hdf['open']]
df['range'] = hdf1.apply(lambda row: calcChange(row['open'], row['close']), axis=1)
result.append(["高开高走，收盘平均涨幅",  "%.2f%%" %(df['range'].mean())])

df['range'] = hdf1.apply(lambda row: calcChange(row['open'], row['high']), axis=1)
result.append(["高开高走，最大平均涨幅",  "%.2f%%" %(df['range'].mean())])

df['range'] = hdf1.apply(lambda row: calcChange(row['open'], row['low']), axis=1)
result.append(["高开高走，最大平均回撤",  "%.2f%%" %(df['range'].mean())])

result.append(["高开低走概率",  "%.2f%%" %((count - upCount)/count * 100)])

hdf2 = hdf[hdf['close'] < hdf['open']]
df['range'] = hdf2.apply(lambda row: calcChange(row['open'], row['close']), axis=1)
result.append(["高开低走，收盘平均跌幅",  "%.2f%%" %(df['range'].mean())])

df['range'] = hdf2.apply(lambda row: calcChange(row['open'], row['low']), axis=1)
result.append(["高开低走，最大平均跌幅",  "%.2f%%" %(df['range'].mean())])

df['range'] = hdf2.apply(lambda row: calcChange(row['open'], row['high']), axis=1)
result.append(["高开低走，最大平均反弹",  "%.2f%%" %(df['range'].mean())])

## 低开走势
hdf = df[df['open'] < df['pre_close']]
count = hdf.iloc[:,0].size
upCount = hdf[hdf['close'] > hdf['open']].iloc[:,0].size

result.append(["低开高走概率",  "%.2f%%" %(upCount/count * 100)])

hdf1 = hdf[hdf['close'] > hdf['open']]
df['range'] = hdf1.apply(lambda row: calcChange(row['open'], row['close']), axis=1)
result.append(["低开高走，收盘平均涨幅",  "%.2f%%" %(df['range'].mean())])

df['range'] = hdf1.apply(lambda row: calcChange(row['open'], row['high']), axis=1)
result.append(["低开高走，最大平均涨幅",  "%.2f%%" %(df['range'].mean())])

df['range'] = hdf1.apply(lambda row: calcChange(row['open'], row['low']), axis=1)
result.append(["低开高走，最大平均回撤",  "%.2f%%" %(df['range'].mean())])

result.append(["低开低走概率",  "%.2f%%" %((count - upCount)/count * 100)])

hdf2 = hdf[hdf['close'] < hdf['open']]
df['range'] = hdf2.apply(lambda row: calcChange(row['open'], row['close']), axis=1)
result.append(["低开低走，收盘平均跌幅",  "%.2f%%" %(df['range'].mean())])

df['range'] = hdf2.apply(lambda row: calcChange(row['open'], row['low']), axis=1)
result.append(["低开低走，最大平均跌幅",  "%.2f%%" %(df['range'].mean())])

df['range'] = hdf2.apply(lambda row: calcChange(row['open'], row['high']), axis=1)
result.append(["低开低走，最大平均反弹",  "%.2f%%" %(df['range'].mean())])

table = AsciiTable(result)
print(table.table)
