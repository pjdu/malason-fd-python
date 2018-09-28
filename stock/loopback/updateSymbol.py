# -*- coding:UTF-8 -*-
# 基础库导入
from __future__ import division
from __future__ import print_function

import warnings

from abupy.MarketBu import ABuDataCache

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import os
import time
import sys

# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy

# 使用实时数据 abupy.env.enable_example_env_ipython()
abupy.env.disable_example_env_ipython()

from abupy import ABuSymbolPd
from abupy import EDataCacheType, EMarketSourceType


def update_data(symbol):
    current_time_format_1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    current_time_format_2 = time.strftime('%Y%m%d', time.localtime(time.time()))

    abupy.env.g_market_source = EMarketSourceType.E_MARKET_SOURCE_nt
    abupy.env.g_data_cache_type = EDataCacheType.E_DATA_CACHE_CSV

    df = ABuSymbolPd.make_kl_df(symbol, n_folds=None, start='2012-01-01', end=current_time_format_1)
    ABuDataCache.save_kline_df(df, symbol, '20120101', current_time_format_2)


symbol = abupy.ABuSymbol.code_to_symbol(sys.argv[1])
update_data(symbol)
