import pandas as pd
from docx.api import Document

document = Document('Table 3Intra.docx')
table = document.tables[0]

data = []

keys = None
for i, row in enumerate(table.rows):
    text = (cell.text for cell in row.cells)

    if i == 0:
        keys = tuple(text)
        continue
    row_data = dict(zip(keys, text))
    data.append(row_data)

df = pd.DataFrame(data)
print(df)

df=df[(df['Run \nDate']=='Intra run SD') | (df['Run \nDate']=='Intra run %CV') | (df['Run \nDate']=='Intra run %Bias') |(df['Run \nDate']=='n')]
print("Print the Values: - Intra run SD, Intra run %CV, Intra run %Bias, n :")
print(df)
