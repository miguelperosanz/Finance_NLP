#Import the dependencies
import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv

#Create two empty lists for the company name and company ticker symbol
company_name =[]
company_ticker = []

#Create a function to scrape the data
def scrape_stock_symbols(Letter):
    Letter =  Letter.upper()
    URL =  'https://www.advfn.com/nyse/newyorkstockexchange.asp?companies='+Letter
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    odd_rows = soup.find_all('tr', attrs= {'class':'ts0'})
    even_rows = soup.find_all('tr', attrs= {'class':'ts1'})
    for i in odd_rows:
        row = i.find_all('td')
        company_name.append(row[0].text.strip())
        company_ticker.append(row[1].text.strip())
    for i in even_rows:
        row = i.find_all('td')
        company_name.append(row[0].text.strip())
        company_ticker.append(row[1].text.strip())

        return (company_name, company_ticker)


#Get and show a list of every letter in the alphabet
import string
string.ascii_uppercase


#Loop through every letter in the alphabet to get all of the tickers from the website
for char in string.ascii_uppercase:
  (temp_name,temp_ticker) = scrape_stock_symbols(char)
  
  
 #Create a new dataFrame that contains the company name and company ticker
data = pd.DataFrame(columns = ['company_name',  'company_ticker']) 
data['company_name'] = company_name
data['company_ticker'] = company_ticker

#Data Cleaning
data = data[data['company_name'] != '']

#Show the data
print(data)

pd.set_option('display.max_rows', None)
data.to_csv (r'symbols.csv', index = False, header=True)
