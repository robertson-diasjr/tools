#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


# Navigate to the URL
url = "https://www.fundsexplorer.com.br/ranking"

try:
    driver.get(url)

    # Find the table element
    table_xpath = '//*[@id="upTo--default-fiis-table"]/div/table'
    table_element = table = driver.find_element(By.XPATH, table_xpath)

    # Get the HTML content of the table
    table_html = table_element.get_attribute("outerHTML")

    # Close the browser
    driver.quit()
    print ("Page successfully loaded")

except:
    print("Page not loaded")


# In[3]:


# Read the HTML table into a Pandas DataFrame
table = pd.read_html(table_html, encoding='utf-8', thousands='.')[0]


# In[4]:


# Column normalization
#
# Remove R$ and %
table.rename(columns=lambda x: x.replace('R$', ''), inplace=True)

# Replace whitespace with underscore
table.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)

# Remove .
table.rename(columns=lambda x: x.replace('.', ''), inplace=True)

# Remove parentheses from column names using lambda and rename
table.rename(columns=lambda x: x.replace('(', ''), inplace=True)
table.rename(columns=lambda x: x.replace(')', ''), inplace=True)

# Uppercase all the names
table.columns = table.columns.str.upper()

# Remove underscore in the end of strings
table.columns = table.columns.str.rstrip('_')

# Remove accents
table.columns = [unidecode(col) for col in table.columns]


# In[5]:


# Rows and columns normalization
#
# Converting all to string for cleanup
table = table.astype('string')

# Number fix
for column in table.columns:
    table[column] = table[column].str.replace('.', '')
    table[column] = table[column].str.replace(',', '.')

# Remove %
table = table.replace('%', '', regex=True)

# Replace <NA> with 0
table = table.fillna('0')

# Converting to float64
maintain_as_string = ['FUNDOS', 'SETOR']
table = table.astype({col: 'float64' for col in table.columns if col not in maintain_as_string})


# In[ ]:


# Filters

# Filtering the columns to evaluate
# ---
columns_filters = ["FUNDOS", "SETOR", "PRECO_ATUAL", "P/VP", "ULTIMO_DIVIDENDO", "DIVIDEND_YIELD", "VARIACAO_PRECO", "LIQUIDEZ_DIARIA"]
table_filtered = table[columns_filters]

# Filtering by FII tickers
# ---
fii_ticker = [ "BCFF11", "BCIA11", "HGFF11", "JSAF11", "KFOF11", "KISU11", "RBRF11", "URPR11", "XPLG11"]
fii_by_ticker = table_filtered[table_filtered['FUNDOS'].isin(fii_ticker)]
#fii_by_ticker = table[table['FUNDOS'].isin(fii_ticker)]
fii_by_ticker.sort_values(by='FUNDOS', ascending=True)

# Filtering by FII Setor
# ---
#fii_setor =["Fundo de Fundos"]
#fii_by_setor = table_filtered[table_filtered['SETOR'].isin(fii_setor)]
#fii_by_setor.shape[0] # Total de fundos listados
#fii_by_setor.sort_values(by='ULTIMO_DIVIDENDO', ascending=False)


# In[ ]:


# Report
# ---
# fii_by_ticker
# fii_by_setor.sort_values(by=['ULTIMO_DIVIDENDO', 'PRECO_ATUAL_BRL'], ascending=[False, True])
# display (table)
# display (table_filtered)


# In[6]:


# Export table to CSV
# table.to_csv('FII_Funds_Explorer.csv', index=False)

# Export table to Excel
table.to_excel('FII_Funds_Explorer.xlsx', index=False)

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

