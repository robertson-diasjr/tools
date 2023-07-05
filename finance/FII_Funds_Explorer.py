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
chrome_options.add_argument("--headless")
service = Service('C:\terraform\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the URL
url = "https://www.fundsexplorer.com.br/ranking"
driver.get(url)

# Find the table element
table_xpath = '//*[@id="upTo--default-fiis-table"]/div/table'
table_element = table = driver.find_element(By.XPATH, table_xpath)

# Get the HTML content of the table
table_html = table_element.get_attribute("outerHTML")

# Close the Selenium webdriver
driver.quit()

# Read the HTML table into a Pandas DataFrame
table = table = pd.read_html(table_html, encoding='utf-8', thousands='.')[0]

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
#exit()