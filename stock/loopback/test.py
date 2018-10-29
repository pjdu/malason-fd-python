from datetime import datetime

import matplotlib.pyplot as plt
import pytz
import seaborn as sns
import talib as ta
from empyrical import cum_returns, annual_return, sharpe_ratio, max_drawdown
from matplotlib.dates import DateFormatter

from zipline import run_algorithm
from zipline.api import symbol, order, record
from zipline.finance import commission, slippage


def initialize(context):
    context.asset = symbol('AAPL')

    context.invested = False

    context.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))

    context.set_slippage(slippage.VolumeShareSlippage(volume_limit=0.025, price_impact=0.1))


def handle_data(context, data):
    trailing_window = data.history(context.asset, ['high', 'low', 'close', 'open'], 40, '1d')

    if trailing_window.isnull().values.any():
        return

    cci = ta.CCI(trailing_window['high'].values, trailing_window['low'].values, trailing_window['close'].values,
                 timeperiod=14)

    buy = False
    sell = False

    if (cci[-1] >= 50) and not context.invested:
        order(context.asset, 100)
        context.invested = True
        buy = True
    elif (cci[-1] < 50) and context.invested:
        order(context.asset, -100)
        context.invested = False
        sell = True

    record(open=data.current(context.asset, "open"),
           high=data.current(context.asset, "high"),
           low=data.current(context.asset, "low"),
           close=data.current(context.asset, "close"),
           cci=cci[-1],
           buy=buy,
           sell=sell)


def analyze(context=None, results=None):
    pass


def draw_return_rate_line(result):
    sns.set_style('darkgrid')
    sns.set_context('notebook')
    ax = plt.axes()
    years_fmt = DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(years_fmt)
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=35, horizontalalignment='right')
    sns.lineplot(x='period_close',
                 y='algorithm_period_return',
                 data=result,
                 label="AAPL")
    sns.lineplot(x='period_close',
                 y='benchmark_period_return',
                 data=result, label="SPX")

    plt.legend(loc='upper left')
    plt.title("return rate of AAPL and SPX")
    plt.xlabel('time')
    plt.ylabel('return rate')
    plt.show()


if __name__ == '__main__':
    capital_base = 10000
    start = datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = datetime(2017, 1, 1, 0, 0, 0, 0, pytz.utc)

    result = run_algorithm(start=start, end=end, initialize=initialize,
                           capital_base=capital_base, handle_data=handle_data,
                           bundle='quandl', analyze=analyze)

    draw_return_rate_line(result)

    return_list = result['returns']

    ann_return = annual_return(return_list)

    cum_return_list = cum_returns(return_list)

    sharp = sharpe_ratio(return_list)

    max_drawdown_ratio = max_drawdown(return_list)
