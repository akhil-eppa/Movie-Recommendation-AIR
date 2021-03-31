# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 12:50:31 2021

@author: Akhil
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_reccomendation(data,movie_name,index,cosine_sim):
    present_index=index[movie_name] # Get necessary mapping
    sim_scores=list(enumerate(cosine_sim[present_index])) # List all cosine similarity values for the particular movie
    sim_scores=sorted(sim_scores, key=lambda x:x[1], reverse=True) #Sort in descending order based on cosine similarity scores
    sim_scores=sim_scores[1:11] #Select top 10
    movie_index=[i[0] for i in sim_scores] #Store movie_id in list
    return data['title'].iloc[movie_index] # Return the title of the movie_index row

def main():
    data=pd.read_csv("tmdb_5000_movies.csv")
    '''
    Recommendation by performing cosine similarity
    on tf-idf vectors generated from the overviews
    of movies. Before performing tf-idf vectorization, define vectorizer to remove english
    stop words
    '''
    tfidf_vectorizer=TfidfVectorizer(stop_words='english')
    '''
    Fill up NA overviews
    '''
    data['overview']=data['overview'].fillna('')
    '''
    Construction of the tf-idf matrix
    It is a sparse matrix:
    (document_id, token_id) , tf_idf score
    '''
    tfidf_matrix=tfidf_vectorizer.fit_transform(data['overview'])
    '''
    Calculating cosine similarity
    '''
    cosine_sim=cosine_similarity(tfidf_matrix,tfidf_matrix)
    print(cosine_sim)
    '''
    Mapping movie titles to index
    '''
    
    index=pd.Series(data.index, index=data['title']).drop_duplicates()
    
    movie_name='The Shawshank Redemption'
    print(get_reccomendation(data,movie_name,index,cosine_sim))
    
if __name__ == "__main__":
    main()
'''
Output for The Shawshank Redemption
531               Civil Brand
3785                    Prison
609                Escape Plan
2868                  Fortress
4727              Penitentiary
1779    The 40 Year Old Virgin
2667          Fatal Attraction
3871         A Christmas Story
434           The Longest Yard
42                 Toy Story 3
'''