#!/usr/bin/env python
# coding: utf-8

# Modulos
# pip install openpyxl pandas unidecode yfinance matplotlib selenium webdriver-manager
import pandas as pd
from unidecode import unidecode
import requests
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Set up Selenium 4 Chrome driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

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
    print ("URL IFIX successfully loaded")

except:
    print("URL IFIX failed")

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
    print ("URL Segment successfully loaded")
    
except:
    print("URL Segment failed")

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
table = table.rename(columns={"COTACAO": "PRECO_COTA"})
table = table.rename(columns={"IFIX_PARTICIPACAO_PERCENTUAL": "PARTICIPACAO_IFIX"})
table = table.rename(columns={"LIQUIDEZ_MEDIA_DIARIA_MES_ATUAL": "LIQUIDEZ"})
table = table.rename(columns={"YIELD_DE_DISTRIBUICAO_1_MES": "DY"})
table = table.rename(columns={"YIELD_DE_DISTRIBUICAO_12_MESES": "DY_12_MESES"})

# Rows and columns normalization
#
# Converting all to string for cleanup
table = table.astype('string')
table_segment = table_segment.astype('string')

# Remove "R$" from all values across all columns
table = table.applymap(lambda x: x.replace('R$', '') if isinstance(x, str) else x)

# Number fix
for column in table.columns:
    table[column] = table[column].str.replace('.', '')
    table[column] = table[column].str.replace(',', '.')
    table[column] = table[column].str.replace('%', '')

# Considering only the stock price instead of % up/down and date
table['PRECO_COTA'] = table['PRECO_COTA'].str.split().str[0]

# Preserve original number format
pd.set_option('display.float_format', '{:.2f}'.format)

# Converting to float64
to_float = ['PRECO_COTA', 'VALOR_PATRIMONIAL', 'VALOR_COTA', 'VALOR_DE_MERCADO', 'VARIACAO_DA_COTA_NO_ANO', 'DY', 'DY_12_MESES', 'P/VPA', 'QTDE_DE_COTISTAS', 'LIQUIDEZ', 'PARTICIPACAO_IFIX']
table[to_float] = table[to_float].apply(pd.to_numeric, errors='coerce')
table[to_float] = table[to_float].astype('float64')

# Merging table
merged_table = pd.merge(table, table_segment)

# Export table to Excel
def export_to_excel():
    try:
        file_to_excel = merged_table
        output_file = "FII_Clube.xlsx"
        file_to_excel.to_excel(output_file, index=False)
        print ("Successfully exported to Excel")
    except:
        print ("Fail to export to Excel")

export_to_excel()

