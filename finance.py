from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline, AutoModel
import torch
import numpy as np 
import re
import requests
from bs4 import BeautifulSoup
    
    
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

classifier = pipeline(task="sentiment-analysis", model=model, tokenizer=tokenizer, return_all_scores=True)

news=[]
word = 'Bitcoin'

for i in range(1,6):

    URL = 'https://newslookup.com/results?p='+ str(i) +'&q='+ word +'&dp=5&mt=-1&ps=10&s=&cat=-1&fmt=&groupby=no&site=&dp=5'
    res = requests.get(URL)
    res.raise_for_status()
    content = res.content
    soup = BeautifulSoup(content, 'html.parser')

    header = soup.find('div', {'id' : 'results'}).find_all('a', {'class' : 'title'})
    subheader = soup.find('div', {'id' : 'results'}).find_all('p', {'class' : 'desc'})


    for headerclean in header:
        news.append(headerclean.text) 

print(news)

rates=[]

for new in news:
    rates.append(classifier(new))
    
    rates_negative=[]

for i in range(len(rates)):
    rates_negative.append(rates[i][0][0]['score'])
    
    
avg_negative = np.average(rates_negative)
avg_positive = 1 - avg_negative

print('negative feeling = ',avg_negative)
print('positive feeling = ',avg_positive)