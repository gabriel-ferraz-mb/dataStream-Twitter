
# Install Libraries
#!pip install textblob
#!pip install tweepy
#!pip install pycountry
#!pip install langdetect
#!pip install keyboard


# Import Libraries
from textblob import TextBlob
from time import sleep 
#import sys
import tweepy
import time
import pandas as pd
#import numpy as np
#import os
#import nltk
#import pycountry
#import re
#import string
import keyboard
#from wordcloud import WordCloud, STOPWORDS
#from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#from langdetect import detect
#from nltk.stem import SnowballStemmer
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
#from sklearn.feature_extraction.text import CountVectorizer


# Authentication
consumerKey = "0WSOZr7dkbcr96pgZVgrFBLrj"
consumerSecret = "zO8HEiftTLZxhxQNTji4E1XHRNVyAsv97wFpHxAgntoBOqtqMj"
accessToken = "1269796100116041730-rUcwrXHwMfusOg0HOmQRuisWWdbaxn"
accessTokenSecret = "AFY2UrEblASPf9XEdLmP2BgyDm6gE1HCkHTkiTGwXHbNm"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)


keyword   = input("Please enter keyword or hashtag to search: ")
noOfTweet = int(input ("Please enter how many tweets to analyze..: "))

#Sentiment Analysis

def percentage(part,whole):
    return 100 * float(part)/float(whole)

while keyboard.is_pressed("esc") == False:

    tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(noOfTweet)
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    neutral_list = []
    negative_list = []
    positive_list = []
    

    for tweet in tweets:
        
        tweet_list.append(tweet.text)
        analysis = TextBlob(tweet.text)
        score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
        neg = score["neg"]
        neu = score["neu"]
        pos = score["pos"]
        comp = score["compound"]
        polarity += analysis.sentiment.polarity

        if neg > pos:
            negative_list.append(tweet.text)
            negative += 1
        elif pos > neg:
            positive_list.append(tweet.text)
            positive += 1
        elif pos == neg:
            neutral_list.append(tweet.text)
            neutral += 1

    positive = percentage(positive, noOfTweet)
    negative = percentage(negative, noOfTweet)
    neutral = percentage(neutral, noOfTweet)
    polarity = percentage(polarity, noOfTweet)
    positive = format(positive, ".1f")
    negative = format(negative, ".1f")
    neutral = format(neutral, ".1f")


    #Number of Tweets (Total, Positive, Negative, Neutral)
    tweet_list = pd.DataFrame(tweet_list)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)
    print("------------------------")
    print("total number...: ",len(tweet_list))
    print("positive number: ",len(positive_list))
    print("negative number: ", len(negative_list))
    print("neutral number.: ",len(neutral_list))

    sleep(60) 



#Creating PieCart
#labels = ['Positive ['+str(positive)+'%]' , 'Neutral ['+str(neutral)+'%]','Negative ['+str(negative)+'%]']
#sizes = [positive, neutral, negative]
#colors = ['yellowgreen', 'blue','red']
#patches, texts = plt.pie(sizes,colors=colors, startangle=90)
#plt.style.use('default')
#plt.legend(labels)
#plt.title('Sentiment Analysis Result for keyword= '+keyword+'' )
#plt.axis('equal')
#plt.show()


