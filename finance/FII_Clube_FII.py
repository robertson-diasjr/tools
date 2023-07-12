#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from unidecode import unidecode
import sqlite3

# Set up Selenium Chrome driver
chrome_options = Options()
chrome_options.add_argument("--headless=new")
service = Service('C:\terraform\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the URL to get all the accounts
try:
    url = "https://www.clubefii.com.br/fundos-imobiliarios/39950/IFIX"
    driver.get(url)

    # Find the table element
    table_xpath = '//*[@id="tabela_profile"]'
    table_element = table = driver.find_element(By.XPATH, table_xpath)

    # Get the HTML content of the table
    table_html = table_element.get_attribute("outerHTML")
    
    # Building the DataFramework
    table = pd.read_html(table_html, encoding='utf-8', thousands='.')[0]

    # Close the browser
    driver.quit()
    print ("Page IFIX successfully loaded")

except:
    print("Page IFIX failed")

# Navigate to the URL to get all the segments
try:
    import requests    
    url_segment = "https://www.clubefii.com.br/fundo_imobiliario_lista"
        
    headers = {
        'User-Agent': 
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }

    request_segment = requests.get(url_segment, headers=headers)
        
    if request_segment.status_code == 200:
        # Building the DataFramework
        table_segment = pd.read_html(request_segment.text, encoding='utf-8')[0]
        # Extracting the required tables
        table_segment = table_segment[['CÓDIGO', 'SEGMENTO']]
    
    print ("Page Segment successfully loaded")
    
except:
    print("Page Segment failed")

# Column normalization
#

# Remove "R$" and "-" "and replace whitespace with underscore
table.rename(columns=lambda x: x.replace('R$', '').replace(' ', '_').replace('-_', ''), inplace=True)
table_segment.rename(columns=lambda x: x.replace('R$', '').replace(' ', '_').replace('-_', ''), inplace=True)

# Uppercase all the names
table.columns = table.columns.str.upper()

# Remove underscore in the end of strings
table.columns = table.columns.str.rstrip('_')
table_segment.columns = table_segment.columns.str.rstrip('_')

# Remove accents
table.columns = [unidecode(col) for col in table.columns]
table_segment.columns = [unidecode(col) for col in table_segment.columns]

# Column naming
table = table.rename(columns={"CODIGO_NEGOCIACAO": "CODIGO"})
table = table.rename(columns={"VALOR_PATRIMONIAL_POR_COTA": "VALOR_COTA"})
table = table.rename(columns={"IFIX_PARTICIPACAO_PERCENTUAL": "PARTICIPACAO_IFIX"})
table = table.rename(columns={"LIQUIDEZ_MEDIA_DIARIA_MES_ATUAL": "LIQUIDEZ"})
table = table.rename(columns={"YIELD_DE_DISTRIBUICAO_1_MES": "DY"})
table = table.rename(columns={"YIELD_DE_DISTRIBUICAO_12_MESES": "DY_12_MESES"})

# Rows and columns normalization
#
# Converting all to string for cleanup
table = table.astype('string')
table_segment = table_segment.astype('string')

# Number fix
for column in table.columns:
    table[column] = table[column].str.replace('R$', '')
    table[column] = table[column].str.replace('.', '')
    table[column] = table[column].str.replace(',', '.')
    table[column] = table[column].str.replace('%', '')
    
# Considering only the stock price instead of % up/down and date
table['COTACAO'] = table['COTACAO'].str.split().str[0]

# Preserve original number format
pd.set_option('display.float_format', '{:.2f}'.format)

# Converting to float64
no_changes = ['CODIGO', 'CODIGO_NEGOCIACAO', 'NOME', 'NOME_DO_FUNDO', 'DATA_IPO', 'ADMINISTRADOR', 'SEGMENTO', 'RELATORIOS_DE_ANALISE', 'FEED']
table = table.astype({col: 'float64' for col in table.columns if col not in no_changes})

# Merging table
merged_table = pd.merge(table, table_segment)

# Changing display view
display_order = ['CODIGO', 'SEGMENTO', 'COTACAO', 'P/VPA', 'VALOR_COTA', 'DY', 'DY_12_MESES', 'VALOR_DE_MERCADO', 'QTDE_DE_COTISTAS', 'LIQUIDEZ', 'PARTICIPACAO_IFIX', 'VARIACAO_DA_COTA_NO_ANO', 
        'VALOR_PATRIMONIAL', 'NOME_DO_FUNDO', 'ADMINISTRADOR', 'DATA_IPO']

display_view = merged_table[display_order]

# Export table to Excel
display_view.to_excel('FII_Clube.xlsx', index=False)

# SQLite function
def export_to_sqlite():
    # Create a connection to the SQLite database
    conn = sqlite3.connect('fii.db')

    # Convert the pandas DataFrame into a SQLite table
    table.to_sql('fii', conn, if_exists='replace', index=False)

    # Close the database connection
    conn.close()

# Export to SQLite
#try:
#    export_to_sqlite()
#    print("Successfully imported into SQLite")
#except:
#    print("Fail to import into SQLite")
#    exit()

