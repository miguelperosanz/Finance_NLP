import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import numpy as np 
import requests
from bs4 import BeautifulSoup
import csv
from datetime import date



#CHOOSING ASSET MENU:
def choosing_asset():
    
    with open('symbols.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    
    option = st.sidebar.selectbox('Select your financial asset (crypto, NYSE, NASDAQ)', data, index=0, format_func=lambda o: o[0] +' (' + o[1] +')')
   
    name = option[0]
    ticker = option[1]
    

    return(name,ticker)

 

#WEBSCRAPING FUNCTION:
def scraping(word, period):
    
    def hours():
        
        for i in range(1,11):
    
            URL = 'https://newslookup.com/results?p='+ str(i) +'&q='+ word +'&dp=5&mt=-1&ps=10&s=&cat=-1&fmt=&groupby=no&site=&dp=5&tp='+ str(number)
                
            res = requests.get(URL)
            res.raise_for_status()
            content = res.content
            soup = BeautifulSoup(content, 'html.parser')
        
            header = soup.find('div', {'id' : 'results'}).find_all('a', {'class' : 'title'})
            #subheader = soup.find('div', {'id' : 'results'}).find_all('p', {'class' : 'desc'})
        
            for headerclean in header:
                news.append(headerclean.text)
        
        return()
    
  
    def years():
        
        for i in range(1,11):
    
            URL = 'https://newslookup.com/results?p='+ str(i) +'&q='+ word +'&dp=5&mt=-1&ps=10&s=&cat=-1&fmt=&groupby=no&site=&dp=5&tp=Y'+ str(year)
            print('URL = ', URL)    
            res = requests.get(URL)
            res.raise_for_status()
            content = res.content
            soup = BeautifulSoup(content, 'html.parser')
        
            header = soup.find('div', {'id' : 'results'}).find_all('a', {'class' : 'title'})
            #subheader = soup.find('div', {'id' : 'results'}).find_all('p', {'class' : 'desc'})
        
            for headerclean in header:
                news.append(headerclean.text)
        
        return()    
    
    
    
    
    
    news=[]
    current_year = date.today().year
    
    if period == '< 36 hours':
        
        for i in range(1,11):
    
            URL = 'https://newslookup.com/results?p='+ str(i) +'&q='+ word +'&dp=5&mt=-1&ps=10&s=&cat=-1&fmt=&groupby=no&site=&dp=5'
            res = requests.get(URL)
            res.raise_for_status()
            content = res.content
            soup = BeautifulSoup(content, 'html.parser')
    
            header = soup.find('div', {'id' : 'results'}).find_all('a', {'class' : 'title'})
            #subheader = soup.find('div', {'id' : 'results'}).find_all('p', {'class' : 'desc'})
    
            for headerclean in header:
                news.append(headerclean.text)
    
    
    elif (period == 'Last hour'):
        number = 1      
        hours()
                
    elif (period == '< 2 hours'):
        number = 2          
        hours()
                
    elif (period == '< 4 hours'):
        number = 4          
        hours()
        
    elif (period == '< 6 hours'):
        number = 6           
        hours()
        
    elif (period == '< 12 hours'):
        number = 12           
        hours()
            
    elif (period == '< 24 hours'):
        number = 24           
        hours()
        
    elif (period == '< 48 hours'):
        number = 48           
        hours()        

    elif (period == '< 72 hours'):
        number = 72           
        hours()
        
    elif (period == '< 7 days'):
        number = 168           
        hours()
        
    elif (period == '< 14 days'):
        number = 336           
        hours()
        
    elif (period == '< 30 days'):
        number = 720           
        hours()
        
    elif (period == '> 30 days ' + str(current_year)):
        number = -720           
        hours()
               
    elif (period == current_year-1):
        year = current_year-1
        years() 
        
    elif (period == current_year-2): 
        year = current_year-2
        years() 
        
    elif (period == current_year-3): 
        year = current_year-3
        years()  

    elif (period == current_year-4):
        year = current_year-4
        years() 
        
    elif (period == current_year-5): 
        year = current_year-5
        years() 
        
    elif (period == current_year-6):
        year = current_year-6
        years() 

    elif (period == current_year-7):
        year = current_year-7
        years() 
        
    elif (period == current_year-8):
        year = current_year-8
        years()     
        

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



#VISUALIZATION POSITIVITY OF THE NEWS:

def visualization_positivity(negative, positive):

          
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


#VISIUALIZATION HISTORICAL VALUES

def visualization_history(ticker, start_date, end_date, chosen_interval):  

    
    
    tickerSymbol = str(ticker)
                
    tickerData = yf.Ticker(tickerSymbol)
                       
                    
    #DATES FOR CLOSE AND VOLUME    
    
                
    tickerDf = tickerData.history(interval=chosen_interval, start=start_date, end=end_date)
    
    print('tickerDf = ', tickerDf)
    
    if tickerDf.empty:

        st.write('Data not available for this period of time and interval. Please modify the parameters')
            
    else:

    
    #CLOSING PRICE
        
        st.write("""# Stock closing price""")
        st.line_chart(data = tickerDf.Close)
        
                
    #VOLUME
        
        st.write("""# Stock volume""")        
        st.line_chart(data = tickerDf.Volume)
    
    
    
    return()


#VISUALIZATION HISTORICAL VALUES MAXIMAL PERIOD


def visualization_history_maxperiod(ticker): 
    
    tickerSymbol = str(ticker)

    tickerData = yf.Ticker(tickerSymbol)
    
    tickerDf_max = tickerData.history(period = "Max")
    
    st.write("""# Stock closing price""")
    
    st.line_chart(data = tickerDf_max.Close)
    
    st.write("""# Stock volume""")
    
    st.line_chart(data = tickerDf_max.Volume)

    return()



# FUNCTION TO DISPLAY EXTRA INFO

def extra_info(ticker):
    
    
    tickerSymbol = str(ticker)

    tickerData = yf.Ticker(tickerSymbol)
    
    
    
    #ACTIONS (DIVIDENDS, SPLITS)
    
    
    st.write("""# Actions (dividends, splits)""", tickerData.actions)
    
    
    #HISTORICAL MARKET DATA
    
    
    st.write("""# Historical market data""", tickerData.history(period="max"))
    
    
    #FINANCIALS
    
    st.write("""# Financials""", tickerData.financials)
    
    st.write("""# Quarterly financials""", tickerData.quarterly_financials)
    
    
    #MAJOR HOLDERS:
            
    st.write("""# Major Holders""", tickerData.major_holders)


    #INSTITUTIONAL HOLDERS:
            
    st.write("""# Institutional Holders""", tickerData.institutional_holders)
    
    
    #BALANCE SHEET
    
    st.write("""# Balance sheet""", tickerData.balance_sheet)
    
    st.write("""# Quarterly balance sheet""", tickerData.quarterly_balance_sheet)
    
    
    #CASHFLOW:
            
    st.write("""# Cashflow""", tickerData.cashflow)
    
    st.write("""# Quarterly cash flow""", tickerData.quarterly_cashflow)
    
    
    
    #EARNINGS:
            
    st.write("""# Earnings""", tickerData.earnings)
    
    st.write("""# Quarterly earnings""", tickerData.quarterly_earnings)
    
    
    #SUSTAINABILITY:
            
    st.write("""# Sustainability""", tickerData.sustainability)
    
    
    #RECOMMENDATIONS:
            
    st.write("""# Recommendations""", tickerData.recommendations)
    
    
    #NEXT EVENTS:
            
    st.write("""# Next event""", tickerData.calendar)
    
    
    
    return()




#MAIN FUNCTION:

def main():
    
    st.sidebar.header("Invest advisor")
    
    
    
    (name,ticker) = choosing_asset()
    
    show_info = st.sidebar.button("Show info") 
    
    if show_info:
        
        st.write("""# Info:""", yf.Ticker(ticker).info)
        
    
    st.sidebar.header("Natural Language Processing")
    
    current_year = date.today().year
 
    period = st.sidebar.selectbox('Period of the news',('Last hour','< 2 hours','< 4 hours','< 6 hours','< 12 hours','< 24 hours',
    '< 36 hours','< 48 hours','< 72 hours','< 7 days','< 14 days','< 30 days','> 30 days ' + str(current_year), current_year-1, 
    current_year-2, current_year-3, current_year-4, current_year-5, current_year-6, current_year-7, current_year-8))    
    
    
    result_news = st.sidebar.button("Scrape news and analyze sentiment")   
    
    
    st.sidebar.header("Historical graphs")
    
    historical_values_max_button = st.sidebar.button("Historical totals")
    
    start_date = st.sidebar.date_input('Start Date (year/month/day)')
    end_date = st.sidebar.date_input('End Date (year/month/day)')
    chosen_interval = st.sidebar.selectbox('Select the interval',('1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo'))
        
    
    historical_values = st.sidebar.button("Historical values in the given period")
    

    
    st.sidebar.header("Extra info")
    
    extra_features = st.sidebar.button("Show extra info")



    if result_news:
        
        
    
        news = scraping(name, period) 

        (negative_feeling, positive_feeling) = getting_feeling(news)

        visualization_positivity(negative_feeling, positive_feeling)
        

        st.write(news)
        


    if historical_values:
        
        visualization_history(ticker, start_date, end_date, chosen_interval)
        
        
    if historical_values_max_button:
        
        visualization_history_maxperiod(ticker)
      
        

    if extra_features:
        
        extra_info(ticker)
        
        
    st.sidebar.header("About")
    
    st.sidebar.info('This an open source project. The source code is publicly available on [GitHub](https://github.com/miguelperosanz/Finance_NLP).') 
    
    about_me = st.sidebar.button('About me')
    
    if about_me:
        
        st.write('Hi, my name is Miguel and this is my little tool to help the people to invest in the stock market and \
                 cryptocurrencies, a topic that I have been interested in since many years ago. The tool has been developed in Python and uses Natural \
                Language Processing and technical analysis. For the NLP part I have used \
                the [distilbert-base-uncased-finetuned](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english) \
                pretrained model from Hugging Face. The tool scrapes an asset news from the webpage https://newslookup.com\
                using [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) and then the model analyzes the positivity of the news. I did a [little \
                study](https://github.com/miguelperosanz/Finance_NLP/blob/main/Screenshot%20from%202021-06-11%2000-21-00.png?raw=true) about the efectivity of different models on different headlines. \
                For the technical analysis I used the [yahoo finances library](https://pypi.org/project/yfinance/) For the design and visualization \
                I used the fantastic library [Streamlit](https://streamlit.io/) for Python, widely used for data science projects. I hope you like the tool. \
                For any comment or suggestion feel free to contact me on migueldeperosanz@yahoo.es. Take care!')

          


if __name__ == "__main__":
    main()
