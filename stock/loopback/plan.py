# 基础库导入

from __future__ import division
from __future__ import print_function

import warnings

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
from terminaltables import AsciiTable

file_path = "PLAN.csv"
f = open(file_path)
df = pd.read_csv(f)
head = list(df)
nr = df.values.tolist()
c = np.vstack((head, nr)).tolist()
table = AsciiTable(c)
print(table.table)
