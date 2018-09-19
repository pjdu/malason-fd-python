# pip install terminaltables
import tushare as ts
import numpy as np
from terminaltables import AsciiTable

df = ts.get_index()
head = list(df)
nr = df.values.tolist()
c=np.vstack((head, nr)).tolist()
table = AsciiTable(c)
print(table.table)
print('\n')

df = ts.get_realtime_quotes(['600188', '600763'])[['code','name','price','bid','ask','volume','amount','time']]
head = list(df)
nr = df.values.tolist()
c=np.vstack((head, nr)).tolist()
table = AsciiTable(c)
print(table.table)
