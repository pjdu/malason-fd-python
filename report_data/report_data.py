import time
import tushare as ts
from pyecharts import Bar, Page

ts.set_token('9c4af04257e55b3f490d14ac46c00cd71383ed0846d8e10694907926')
pro = ts.pro_api()

"""
财报数据
"""

ts_code = '601012.SH'
ts_name = '隆基股份'
startDate = '20150101'
endDate = time.strftime('%Y%m%d', time.localtime(time.time()))
page = Page()

df = pro.income(ts_code=ts_code, start_date=startDate, end_date=endDate)
df = df.sort_values(by="ann_date", ascending=True)

bar = Bar('利润表', width=1600, height=800)
bar.add('营业收入', df['ann_date'], df['revenue'], is_label_show=True)
bar.add('营业利润', df['ann_date'], df['operate_profit'], is_label_show=True)
bar.add('净利润', df['ann_date'], df['n_income_attr_p'], is_label_show=True)
bar.add('基本EPS', df['ann_date'], df['basic_eps'], is_label_show=True)
bar.add('稀释EPS', df['ann_date'], df['diluted_eps'], is_label_show=True)
page.add_chart(bar)

df = pro.balancesheet(ts_code=ts_code, start_date=startDate, end_date=endDate)
df = df.sort_values(by="ann_date", ascending=True)

bar = Bar('资产负债表', width=1600, height=800)
bar.add('总资产', df['ann_date'], df['total_assets'], is_label_show=True)
bar.add('总负债', df['ann_date'], df['total_liab'], is_label_show=True)
page.add_chart(bar)

df = pro.cashflow(ts_code=ts_code, start_date=startDate, end_date=endDate)
df = df.sort_values(by="ann_date", ascending=True)

bar = Bar('现金流量表', width=1600, height=800)
bar.add('经营现金流', df['ann_date'], df['n_cashflow_act'], is_label_show=True)
bar.add('投资现金流', df['ann_date'], df['n_cashflow_inv_act'], is_label_show=True)
bar.add('筹资现金流', df['ann_date'], df['stot_cash_in_fnc_act'], is_label_show=True)
page.add_chart(bar)

page.render("report_data.html")
