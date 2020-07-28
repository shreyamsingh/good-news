import requests
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
import re, string
from nltk.corpus import stopwords
from nltk import FreqDist, classify, NaiveBayesClassifier
from nltk.tokenize import word_tokenize
import pandas as pd
from io import StringIO
import pickle
from datetime import date, timedelta, datetime
import os

f = open('classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

def remove_noise(tweet_tokens, stop_words = ()):
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token =  re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())
    return cleaned_tokens

def getProbs(text):
    tokens = remove_noise(word_tokenize(text))
    output = classifier.classify(dict([token, True] for token in tokens))
    dist = classifier.prob_classify(dict([token, True] for token in tokens))
    return dist.prob("Positive")

def makeDF(df, query):
    api_key = os.environ['NEWS_API_KEY']
    today = date.today()
    week_ago = today - timedelta(days=7)
    url = (r'https://newsapi.org/v2/everything?q=' + query + " NOT pandemic NOT dies" + r'&from=' + str(week_ago) + r'&to=' + str(today) + r'&sortBy=popularity&excludeDomains=techcrunch.com,theverge.com,theinventory.com,gizmodo.com&apiKey=' + api_key)

    response = requests.get(url).json()
    for article in response["articles"]:
        #overallSent = (getProbs(article["title"]) + getProbs(article["content"]) + getProbs(article["description"]))/3
        overallSent = getProbs(article["title"])
        to_append = [article["title"], article["description"], article["content"], article["url"], article["source"]["name"], article["urlToImage"], overallSent, datetime.strptime(article["publishedAt"][0:10], '%Y-%m-%d')]
        df.loc[len(df)] = to_append
    return df

def getData():
    df = pd.DataFrame(columns=["Title", "Description", "Content", "URL", "Source", "imgURL", "Sentiment", "Date"])
    df = makeDF(df, "happy")
    df = makeDF(df, "good")
    to_append = ["", "", "", "", "", "", 0, datetime.today()]
    df.loc[len(df)] = to_append
    df.drop_duplicates(subset=["Title"], keep="first", inplace=True)
    df = df.sort_values(by=['Sentiment'])
    df = df.reset_index(drop=False)
    #print(df.head())
    df.to_pickle("tmp/data.pickle")
#getData()
