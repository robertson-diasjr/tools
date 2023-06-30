#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd

url_A = "https://www.clubefii.com.br/fundo_imobiliario_lista"
url_B = "https://www.clubefii.com.br/fundos_imobiliarios_ranking"
headers = {
    'User-Agent': 
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36'
        ' (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}

request_A = requests.get(url_A, headers=headers)
if request_A.status_code == 200:
    table_A = pd.read_html(request_A.text, encoding='utf-8')[0]

request_B = requests.get(url_B, headers=headers)
if request_B.status_code == 200:
    table_B = pd.read_html(request_B.text, encoding='utf-8')[0]

# Replace comma by dots in both tables
table_A = table_A.replace(',', '.', regex=True)
table_B = table_B.replace(',', '.', regex=True)

# Replace N/D by 0 in both tables
table_A = table_A.replace('N/D', 0)
table_B = table_B.replace('N/D', 0)

# Remove 'R$' and '%'
table_A = table_A.replace(['R\$', '%'], '', regex=True)
table_B = table_B.replace(['R\$', '%'], '', regex=True)

# Remove date fields in table A
table_A = table_A.replace("\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}", "", regex=True)

# Remove column A and B from table A
table_A = table_A.drop(['FEED', 'DATA IPO', 'VALOR IPO', 'RELATÓRIOS DE ANÁLISE'], axis=1)

# Remove column C and D from table B
table_B = table_B.drop(['NOME', 'FEED', 'VARIAÇÃO COTA  DESDE IPO', 'YIELD  1 MES'], axis=1)

# Merge table A and table B
merged_table = pd.merge(table_A, table_B)

# Display on screen
#print (merged_table)

# Export merged table to CSV or Excel
#merged_table.to_csv('FII_Clube.csv', index=False)
merged_table.to_excel('FII_Clube.xlsx', index=False)

print('Success')
