from terminaltables import AsciiTable
import numpy as np

"""
通用工具类
"""

# 打印dataFrame数据
def print_df(df):
    head = list(df)
    nr = df.values.tolist()
    c = np.vstack((head, nr)).tolist()
    table = AsciiTable(c)
    print(table.table)

# 计算平均值，保留两位小数
def average_range(df):
    if df is None:
        return 0

    return round(df.mean(), 2)