import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline, AutoModel
import torch
import numpy as np 
import re
import requests
from bs4 import BeautifulSoup
import csv
from plotly import graph_objs as go
import pandas as pd
from datetime import datetime


#CHOOSING ASSET MENU:
    
def choosing_asset():
    
    with open('symbols.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)


    option = st.selectbox('Select your asset',data)
    st.write('You selected:', option)

    name = option[0]
    ticker = option[1]

    return(name,ticker)



#WEBSCRAPING FUNCTION:

def scraping(word):
    
#    result_news = st.button("scrape news and calculate positivity/negativity")
    
    #st.write (result_news)
    
    news=[]
    
#    if result_news:
    
        
    for i in range(1,2):

        URL = 'https://newslookup.com/results?p='+ str(i) +'&q='+ word +'&dp=5&mt=-1&ps=10&s=&cat=-1&fmt=&groupby=no&site=&dp=5'
        res = requests.get(URL)
        res.raise_for_status()
        content = res.content
        soup = BeautifulSoup(content, 'html.parser')

        header = soup.find('div', {'id' : 'results'}).find_all('a', {'class' : 'title'})
        subheader = soup.find('div', {'id' : 'results'}).find_all('p', {'class' : 'desc'})

        for headerclean in header:
            news.append(headerclean.text)   
           
    return (news)



#GETTING SENTIMENTS FUNCTION:

def getting_feeling(group_of_news):
    
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    classifier = pipeline(task="sentiment-analysis", model=model, tokenizer=tokenizer, return_all_scores=True)

    rates=[]

    for new in group_of_news:
        rates.append(classifier(new))

    rates_negative=[]

    for i in range(len(rates)):
        rates_negative.append(rates[i][0][0]['score'])

    avg_negative = np.average(rates_negative)
    avg_positive = 1 - avg_negative
    
    return (avg_negative, avg_positive)



#VISUALIZATION FUNCTION:

def visualization_positivity(negative,positive):
    
    #POSITIVITY PIECHART
    
    st.write("""
    # Positivity in the news during the last 36 hours:
    """)
             
    
            
    labels = 'Negativity', 'Positivity'
    sizes = [negative, positive]
    explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()
    
    st.pyplot(fig1)
    
    return()


def visualization_history(ticker):    
    
    #HISTORICAL PRICES
    
    tickerSymbol = str(ticker)
    
#    historical_values = st.button("show historical values")
    
    #if historical_values:
    
    
    
    
    tickerData = yf.Ticker(tickerSymbol)

    
    tickerDf = tickerData.history(period='1d', start='2000-01-01', end='2021-01-01')
    
    
    st.write("""# Stock closing price""")
    
    st.line_chart(tickerDf.Close)
    
    st.write("""# Stock volume""")
    
    st.line_chart(tickerDf.Volume)
    

    return()



#MAIN FUNCTION:

def main():
    
    (name,ticker) = choosing_asset()
    
    
    result_news = st.button("scrape news and calculate positivity/negativity")    
    historical_values = st.button("show historical values")
    
    if result_news:
    
        news = scraping(name) 
    
#    print(news)
        (negative_feeling, positive_feeling) = getting_feeling(news)

        visualization_positivity(negative_feeling,positive_feeling)


    if historical_values:

        visualization_history(ticker)

if __name__ == "__main__":
    main()
