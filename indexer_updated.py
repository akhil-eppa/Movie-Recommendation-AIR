# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 22:05:41 2021

@author: Akhil
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 12:32:04 2021

@author: Akhil
"""
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re
stop_words=set(stopwords.words('english'))
stemmer=PorterStemmer()
lemmatizer=WordNetLemmatizer()
def remove_punc(text):
    text=[(i,re.sub(r'[^\w\s]','',word)) for i,word in text]
        
    #text=re.sub(r'[^\w\s]','',text)
    return text
def word_split(text):
    text=text.split(' ')
    return text

def word_normalize(text):
    text=[(i,word.lower()) for i, word in text]
    return text

def remove_stopwords(text):
    filtered_sentence=[(i,word) for i, word in text if not word in stop_words and len(word)>=3]
    return filtered_sentence

def word_stemmer(text):
    text=[(i,stemmer.stem(word)) for i, word in text]
    return text

def word_lemmatizer(text):
    text=[(i,lemmatizer.lemmatize(word)) for i, word in text]
    return text

def word_preprocess(text):
    text=word_with_index(text)
    text=remove_punc(text)
    #text=word_split(text)
    text=word_normalize(text)
    text=remove_stopwords(text)
    text=word_stemmer(text)
    text=word_lemmatizer(text)
    return text

def word_with_index(text):
    word_list=[]
    wcurrent=[]
    windex=None
    for i,c in enumerate(text):
        if c.isalnum():
            wcurrent.append(c)
            windex=i
        elif wcurrent:
            word=u''.join(wcurrent)
            word_list.append((windex-len(word)+1,word))
            wcurrent=[]
    if wcurrent:
        word=u''.join(wcurrent)
        word_list.append((windex-len(word)+1,word))
    return word_list

def inverted_index(text):
    index={}
    for i,word in text:
        loc=index.setdefault(word,[])
        loc.append(i)
    return index

def inverted_index_add(index, movie_id, movie_index):
    for word, locations in movie_index.items():
        indices = index.setdefault(word, {})
        indices[movie_id]=locations
    return index

def main():
    dataset=pd.read_csv("tmdb_5000_movies.csv")
    #dataset=pd.read_csv("tmdb_5000_movies.csv","r")
    names=dataset['original_title']
    dataset['overview']=dataset['overview'].fillna('')
    overviews=dataset['overview']
    #print(word_with_index(overviews[0]))
    x=overviews[0]
    #x=word_with_index(x)
    x=word_preprocess(x)
    
    
    #print(x)
    #l=inverted_index(x)
    #print(l)
    
    index={}
    movies={}
    for i in range(1,len(names)):
        movies[names[i]]=overviews[i]
    for movie_id,text in movies.items():
        text=word_preprocess(text)
        movie_index=inverted_index(text)
        inverted_index_add(index, movie_id, movie_index)
    print(index)
    
main()