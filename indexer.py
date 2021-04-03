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
import json

stop_words=set(stopwords.words('english'))
stemmer=PorterStemmer()
lemmatizer=WordNetLemmatizer()
def remove_punc(text):
    text=[(i,re.sub(r'[^\w\s]','',word)) for i,word in text] # ^\w\s indicates symbols that are NOT \w(A-Za-z0-9_) and \s(whitespace,\t,etc)
        
    #text=re.sub(r'[^\w\s]','',text)
    return text
def word_split(text):
    text=text.split(' ')
    return text

def word_normalize(text): #Convert to lowercase
    text=[(i,word.lower()) for i, word in text]
    return text

def remove_stopwords(text): # Not in predefined list of stopwords and length ofword is greater than 3
    filtered_sentence=[(i,word) for i, word in text if not word in stop_words and len(word)>=3]
    return filtered_sentence

def word_stemmer(text):
    text=[(i,stemmer.stem(word)) for i, word in text]
    return text

def word_lemmatizer(text):
    text=[(i,lemmatizer.lemmatize(word)) for i, word in text]
    return text

def word_preprocess(text):
    text=word_with_index(text) #Returns indexed list of valid words (alphanumeric characters only)
    text=remove_punc(text)
    #text=word_split(text) #Needed?
    text=word_normalize(text) #Convert to lowercase
    text=remove_stopwords(text)
    text=word_stemmer(text) #Chop of unnecessary string of characters
    text=word_lemmatizer(text) #Use of vocabulary to simplify meanings
    return text

def word_with_index(text): #Function splits the words in the overview (valid words with alphanumeric characters only)
    word_list=[]
    wcurrent=[]
    windex=None
    for i,c in enumerate(text): # ennumerate returns index(default=0) followed by the set of characters of the word
        if c.isalnum(): # All characters in the string are alphanumeric
            wcurrent.append(c)
            windex=i
        elif wcurrent: # End of word
            word=u''.join(wcurrent) # Prefix u is for Unicode formatting. Here we join all the characters in the word
            word_list.append((windex-len(word)+1,word)) # Word correctly indexed into the list
            wcurrent=[] 
    if wcurrent: #End of overview
        word=u''.join(wcurrent)
        word_list.append((windex-len(word)+1,word))
    return word_list

def inverted_index(text):
    index={}
    for i,word in text:
        loc=index.setdefault(word,[]) # For every unique word create a list by default
        loc.append(i) # Add the location/position/index
    return index # Dictionary with the words/tokens as keys and their positions in the document as value 

def inverted_index_add(index, movie_id, movie_index):
    for word, locations in movie_index.items():
        indices = index.setdefault(word, {})
        indices[movie_id]=locations
    return index # Dictionary with the words/tokens as keys and value is another dictionary with docID as key and posting list as value

def main():
    dataset=pd.read_csv("tmdb_5000_movies.csv") # To be uncommented while testing only
    names=dataset['original_title']
    dataset['overview']=dataset['overview'].fillna('')
    overviews=dataset['overview']
    #print(word_with_index(overviews[0]))
    #x=overviews[0] #Complete overview text (0 is only for the 1st movie)
    #x=word_with_index(x)
    #x=word_preprocess(x) #Split into words, remove puctuatuion, normalize, remove stopwords, lemmitizing  and stemming
    
    
    #print(x)
    #l=inverted_index(x)
    #print(l)
    
    index={}
    movies={}
    for i in range(1,4):
        movies[names[i]]=overviews[i]
    for movie_id,text in movies.items():
        text=word_preprocess(text)
        movie_index=inverted_index(text)
        inverted_index_add(index, movie_id, movie_index)
    print(index)
    

    with open('index.json', 'w') as fp:
        json.dump(index, fp)

main()