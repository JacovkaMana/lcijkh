import pandas as pd

#df = pd.DataFrame()
#print(type(df))

def read_df()  -> pd.DataFrame:
    df = pd.read_csv('Full_16_09_22.csv', sep='$')
    print(df.iloc[:2])
    return df
