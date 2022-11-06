import pandas as pd

df = pd.read_csv('Full_16_09_22.csv', on_bad_lines='skip')

print(df.iloc[:2])