#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

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
table_html = table_element.get_attribute('outerHTML')

# Close the Selenium webdriver
driver.quit()

# Read the HTML table into a Pandas DataFrame
table = df = pd.read_html(table_html, encoding='utf-8', thousands='.')[0]

# Remove column A and B from table A
table = table.drop(['DY (3M) Acumulado', 'DY (6M) Acumulado', 'DY (3M) média', 'DY (6M) média'], axis=1)

# Display on screen
#print (table)

# Export merged table to CSV or Excel
#table.to_csv('FII_Funds_Explorer.csv', index=False)
table.to_excel('FII_Funds_Explorer.xlsx', index=False)

print ('Success')

