# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 12:50:31 2021

@author: Akhil
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_reccomendation(data,movie_name,index,cosine_sim):
    present_index=index[movie_name]
    sim_scores=list(enumerate(cosine_sim[present_index]))
    sim_scores=sorted(sim_scores, key=lambda x:x[1], reverse=True)
    sim_scores=sim_scores[1:11]
    movie_index=[i[0] for i in sim_scores]
    return data['title'].iloc[movie_index]

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
    '''
    Mapping movie titles to index
    '''
    
    index=pd.Series(data.index, index=data['title']).drop_duplicates()
    
    movie_name='The Shawshank Redemption'
    print(get_reccomendation(data,movie_name,index,cosine_sim))
    
if __name__ == "__main__":
    main()