from terminaltables import AsciiTable
import numpy as np

def print_df(df):
    head = list(df)
    nr = df.values.tolist()
    c = np.vstack((head, nr)).tolist()
    table = AsciiTable(c)
    print(table.table)
