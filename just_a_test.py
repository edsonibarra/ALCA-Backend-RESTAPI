import pandas as pd

filename = 'casas.xlsx'
df = pd.read_excel(filename, sheet_name='CASAS VENTA')

print(df.iloc[0])