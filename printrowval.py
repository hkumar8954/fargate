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
# print('Value of row- Intra run SD:')
# df = df.loc[df['Run \nDate'] == 'Intra run SD']
# print(df)
#
# print('Value of row- Intra run %CV:')
# df = df.loc[df['Run \nDate'] == 'Intra run %CV']
# print(">>>>>>>>>>>>>",df)
# print('Value of row- Intra run %Bias:')
# df = df.loc[df['Run \nDate'] == 'Intra run %Bias']
# print(">>>>>>>>>>>>>",df)
# print('Value of row- n:')
# df = df.loc[df['Run \nDate'] == 'n']
# print(">>>>>>>>>>>",df)
