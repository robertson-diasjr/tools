#!/usr/bin/env python
# coding: utf-8

# In[14]:


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


# In[15]:


# Navigate to the URL
url = "https://www.clubefii.com.br/fundos-imobiliarios/39950/IFIX"

try:
    driver.get(url)

    # Find the table element
    table_xpath = '//*[@id="tabela_profile"]'
    table_element = table = driver.find_element(By.XPATH, table_xpath)

    # Get the HTML content of the table
    table_html = table_element.get_attribute("outerHTML")

    # Close the browser
    driver.quit()
    print ("Page successfully loaded")

except:
    print("Page not loaded")


# In[16]:


# Read the HTML table into a Pandas DataFrame
table = pd.read_html(table_html, encoding='utf-8', thousands='.')[0]


# In[17]:


# Column normalization
#
# Remove R$
# Remove -
# Replace whitespace with underscore
table.rename(columns=lambda x: x.replace('R$', '').replace(' ', '_').replace('-_', ''), inplace=True)

# Uppercase all the names
table.columns = table.columns.str.upper()

# Remove underscore in the end of strings
table.columns = table.columns.str.rstrip('_')

# Remove accents
table.columns = [unidecode(col) for col in table.columns]


# In[18]:


# Rows and columns normalization
#
# Converting all to string for cleanup
table = table.astype('string')

# Number fix
for column in table.columns:
    table[column] = table[column].str.replace('R$', '')
    table[column] = table[column].str.replace('.', '')
    table[column] = table[column].str.replace(',', '.')
    table[column] = table[column].str.replace('%', '')
    
# Considering only the stock price instead of % up/down and date
table['COTACAO'] = table['COTACAO'].str.split().str[0]

# Replace <NA> with 0
#table = table.fillna('0')

# Preserve original number format
pd.set_option('display.float_format', '{:.2f}'.format)

# Convert to float
#to_float = ['COTACAO', 'VALOR_PATRIMONIAL', 'VALOR_PATRIMONIAL_POR_COTA', 'VALOR_DE_MERCADO', 'LIQUIDEZ_MEDIA_DIARIA_MES_ATUAL']
#table[to_float] = table[to_float].astype('float64')

# Converting to float64
no_changes = ['CODIGO_NEGOCIACAO', 'NOME_DO_FUNDO', 'DATA_IPO', 'ADMINISTRADOR']
table = table.astype({col: 'float64' for col in table.columns if col not in no_changes})


# In[19]:


# Export table to Excel
table.to_excel('FII_Clube.xlsx', index=False)

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

