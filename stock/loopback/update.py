# -*- coding:UTF-8 -*-
# 基础库导入
from __future__ import print_function
from __future__ import division

import warnings

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os
import sys
import time
import sys

# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy

# 使用实时数据 abupy.env.enable_example_env_ipython()
abupy.env.disable_example_env_ipython()

from abupy import abu, EMarketTargetType, AbuMetricsBase, ABuMarketDrawing, ABuProgress, ABuSymbolPd, get_price, \
    ABuIndustries
from abupy import EMarketDataFetchMode, EDataCacheType, EMarketSourceType, FuturesBaseMarket, TCBaseMarket, ABuDateUtil
from abupy import AbuDataParseWrap, StockBaseMarket, SupportMixin, ABuNetWork, Symbol, code_to_symbol

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

def update_data(market_target):
    current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    # 切换至腾讯数据源，然后进行全市场更新
    abupy.env.g_market_source = EMarketSourceType.E_MARKET_SOURCE_nt
    abupy.env.g_data_cache_type = EDataCacheType.E_DATA_CACHE_CSV

    for case in switch(market_target):
        if case('us'):
            abu.run_kl_update(start='2012-01-01', end=current_time, market=EMarketTargetType.E_MARKET_TARGET_US, n_jobs=20)
            break
        if case('hk'):
            abu.run_kl_update(start='2012-01-01', end=current_time, market=EMarketTargetType.E_MARKET_TARGET_HK, n_jobs=20)
            break
        if case():
            abu.run_kl_update(start='2012-01-01', end=current_time, market=EMarketTargetType.E_MARKET_TARGET_CN, n_jobs=20)


update_data(sys.argv[1])

