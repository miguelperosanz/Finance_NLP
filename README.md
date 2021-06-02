# Natural Language Processing and sentiment analysis applied to finances


This project uses a Machine Learning model based in Natural Language Processing for helping the people to invest in the stock and crypto market.

The user will type the word with the name of the asset ((variable "word", examples: 'Bitcoin', 'Ethereum', 'Google', 'Apple'...). The script scrapes news connected with the given asset from the web "Newslookup.com". Afterwards, the model "distilbert-base-uncased-finetuned-sst-2-english" is applied in order to get the sentiment of the scraped news. You can find more info about this Natural language processing machine learning model here:

https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english


A negative sentiment would imply a bad moment for investing. A positive sentiment would mean an upward trend.

The tool is being extended by introducing graphs with the historical values of the stock and crypto assets. In the end it is intended to become a tool for helping the investors to make decissions about when buying or selling. The scripts will be converted into a shareable web app by means of the use of streamlit. For the visualization I am using the streamlit library.
