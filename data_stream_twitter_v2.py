#------------------------------------------
#--- Author....: Jaime Leite
#--- Objective.: Stream de Dados do Twitter com MongoDB, Pandas e Scikit Learn
#--- Date......: 7th June 2020
#--- Version...: 1.0
#--- Python Ver: 3.7.6
#--- Details At: 
#------------------------------------------

# Importando os módulos Tweepy, Datetime e Json
from tweepy.streaming import Stream
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime
import json
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
from textblob import TextBlob
os.system('cls')  # on windows
import matplotlib.pyplot as plt
from datetime import datetime
# Importando o módulo Scikit Learn
from sklearn.feature_extraction.text import CountVectorizer
# Importando do PyMongo o módulo MongoClient
from pymongo import MongoClient   
# Importando o módulo Pandas para trabalhar com datasets em Python
import pandas as pd
import keyboard
import time
#------------------------------------------
# Preparando a Conexão com o Twitter
#------------------------------------------
# usuário: falconylistener
# e-mail.: jaime@falcony.com.br
#------------------------------------------

consumer_key = "0WSOZr7dkbcr96pgZVgrFBLrj"
consumer_secret = "zO8HEiftTLZxhxQNTji4E1XHRNVyAsv97wFpHxAgntoBOqtqMj"
access_token = "1269796100116041730-rUcwrXHwMfusOg0HOmQRuisWWdbaxn"
access_token_secret = "AFY2UrEblASPf9XEdLmP2BgyDm6gE1HCkHTkiTGwXHbNm"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

nqtde  = 0
string = "Zelensky"
ntwet  = 200
#outputfile = input("Nome do arquivo de saída ? ")

# Criando uma classe para capturar os stream de dados do Twitter e 
# armazenar no MongoDB

class MyListener(Stream):
    def on_data(self, dados):
   
        global nqtde
        global ntwet
        tweet = json.loads(dados)
        created_at = tweet["created_at"]
        id_str = tweet["id_str"]
        text = tweet["text"]
        obj  = {"created_at":created_at,"id_str":id_str,"text":text,}
        obj2 = {"text":text,}
        tweetind = col.insert_one(obj).inserted_id
        print (obj2)
        print (nqtde)
        nqtde += 1      
        if nqtde == ntwet:
            self.disconnect()
            return False
        else:
            return True
        
                
# Criando o objeto mylistener

mylistener = MyListener(consumer_key, consumer_secret, access_token, access_token_secret)

# Criando o objeto mystream
#mystream = Stream(auth, listener = mylistener)
#mystream = Stream(consumer_key, consumer_secret, access_token, access_token_secret)

#------------------------------------------
# Preparando a Conexão com o MongoDB
#------------------------------------------

resultDf = pd.DataFrame()

# Criando a conexão ao MongoDB
client = MongoClient('localhost', 27017)

# Criando o banco de dados twitterdb
db = client.twitterdb

#while keyboard.is_pressed("esc") == False:
# Criando a collection "col"
col = db.tweets

for i in range(60):
    nqtde  = 0
    # Limpa o banco para o caso dele estar com dados
    db.drop_collection(col)
    
    # Criando uma lista de palavras chave para buscar nos Tweets
    #keywords = ['Big Data', 'Python', 'Data Mining', 'Data Science']
    #keywords = ['PETR4', 'PETR3', 'VALE5', 'ELET3', 'ITUB4', 'BBAS3', 'USIM5', 'BBDC4']
    keywords = [string]
    
    #------------------------------------------
    # Coletando os Tweets
    #------------------------------------------
    
    # Iniciando o filtro e gravando os tweets no MongoDB
    mylistener.filter(track=keywords, languages = ["en"])
    
    #------------------------------------------
    # Consultando os Dados no MongoDB
    #------------------------------------------
    
    mylistener.disconnect()
    
    # Verificando um documento no collection
    col.find_one()
    
    #------------------------------------------
    # Análise de Dados com Pandas e Scikit-Learn
    #------------------------------------------
    
    # criando um dataset com dados retornados do MongoDB
    dataset = [{"created_at": item["created_at"], "text": item["text"],} for item in col.find()]
    
    # Criando um dataframe a partir do dataset 
    df = pd.DataFrame(dataset)
    count = len(df)
    
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    neutral_list = []
    negative_list = []
    positive_list = []
    
    tweets = df['text'].tolist()
    
    for tweet in tweets:
        
        tweet_list.append(tweet)
        analysis = TextBlob(tweet)
        score = SentimentIntensityAnalyzer().polarity_scores(tweet)
        neg = score["neg"]
        neu = score["neu"]
        pos = score["pos"]
        comp = score["compound"]
        polarity += analysis.sentiment.polarity
    
        if neg > pos:
            negative_list.append(tweet)
            negative += 1
        elif pos > neg:
            positive_list.append(tweet)
            positive += 1
        elif pos == neg:
            neutral_list.append(tweet)
            neutral += 1
            
    tweet_list = pd.DataFrame(tweet_list)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)
    
# =============================================================================
#     #Creating PieCart
#     labels = ['Positive ['+str(round((positive/count),4)*100)+'%]' , 'Neutral ['+str(round((neutral/count), 4)*100)+'%]','Negative ['+str(round((negative/count),4)*100)+'%]']
#     sizes = [positive, neutral, negative]
#     colors = ['yellowgreen', 'blue','red']
#     patches, texts = plt.pie(sizes,colors=colors, startangle=90)
#     plt.style.use('default')
#     plt.legend(labels)
#     plt.title("Sentiment Analysis Result for keyword= 'Zelensky'" )
#     plt.axis('equal')
#     plt.show()
# =============================================================================
    
    now = datetime.now()
    d =  {'positive': positive, 'negative': negative, 'neutral': neutral, 'count':count, 'time':now.strftime("%d%m%Y%H%M%S")}
    resultDf = resultDf.append(d, ignore_index=True)
    # Usando o método CountVectorizer para criar uma matriz de documentos
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df.text)
    
    # Contando o número de ocorrências das principais palavras em nosso dataset
    word_count = pd.DataFrame(cv.get_feature_names(), columns=["word"])
    word_count["count"] = count_matrix.sum(axis=0).tolist()[0]
    word_count = word_count.sort_values("count", ascending=False).reset_index(drop=True)
    
    word_count.to_csv(r"C:\Users\gabriel.ferraz\Documents\Pessoal\PECE POLI Data Science & Analytics\DAS 014\wordcount_" +  now.strftime("%d%m%Y%H%M%S") + ".csv", sep=',', index = False) 
    
    time.sleep(900)

resultDf.to_csv(r"C:\Users\gabriel.ferraz\Documents\Pessoal\PECE POLI Data Science & Analytics\DAS 014\result_sentimento.csv", sep=',', index = False)

