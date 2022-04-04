import pandas as pd

df1= pd.read_csv (r'./parse_result.csv')
df2 = df1.replace("CNR",None)
df3 = df2.groupby(["Rank","Name"]).first().reset_index()


df = df3
filled = df.isnull().sum() / len(df)
#print(df.head(20))
print(filled)
df.to_csv(r'./parse_result.csv', na_rep="CNR")