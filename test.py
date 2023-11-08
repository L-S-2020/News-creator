import pandas as pd


df = pd.DataFrame(columns=['a', 'b'])
for i in range(10000):
    df = df._append({'a': 1, 'b': 2}, ignore_index=True)
    df.to_excel("output.xlsx")