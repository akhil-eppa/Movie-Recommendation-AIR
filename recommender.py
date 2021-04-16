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
    '''
    Mapping movie titles to index
    '''
    
    index=pd.Series(data.index, index=data['title']).drop_duplicates()
    
    movie_name='Mission: Impossible - Ghost Protocol'
    print(get_reccomendation(data,movie_name,index,cosine_sim))
    
if __name__ == "__main__":
    main()

'''
Output for Mission: Impossible - Ghost Protocol
134                    Mission: Impossible - Rogue Nation
139                               Mission: Impossible III
2819                                         Act of Valor
213                                Mission: Impossible II
282                                             True Lies
553                                           The Kingdom
425                                   Mission: Impossible
2136                           Team America: World Police
4173    Dr. Strangelove or: How I Learned to Stop Worr...
2229                                        Machete Kills
'''    
    
    
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


'''
Output for Apollo 13
1577             Without a Paddle
3604                    Apollo 18
487                    Red Planet
4411                        Proud
2506                      Madison
4108    In the Shadow of the Moon
3993            Journey to Saturn
373               Mission to Mars
270                   The Martian
1275                     Sunshine
'''

'''
Output for Avatar
3604                       Apollo 18
2130                    The American
634                       The Matrix
1341            The Inhabited Island
529                 Tears of the Sun
1610                           Hanna
311     The Adventures of Pluto Nash
847                         Semi-Pro
775                        Supernova
2628             Blood and Chocolate
'''

'''
Output for Toy Story 3
1541                 Toy Story
343                Toy Story 2
1779    The 40 Year Old Virgin
891            Man on the Moon
3873             Class of 1984
3379              Factory Girl
4387      A LEGO Brickumentary
3065                Heartbeeps
699             Daddy Day Care
1191            Small Soldiers
'''

'''
Output for A LEGO Brickumentary
744           The Lego Movie
42               Toy Story 3
343              Toy Story 2
1704           The Big Short
1191          Small Soldiers
4069             Containment
1965               Footloose
2303          The Nutcracker
2213    Deconstructing Harry
4593                Trekkies
'''

'''
Movies similar to Avengers: Age of Ultron
16                    The Avengers
79                      Iron Man 2
68                        Iron Man
26      Captain America: Civil War
227                 Knight and Day
31                      Iron Man 3
1868            Cradle 2 the Grave
344                    Unstoppable
1922                    Gettysburg
531        The Man from U.N.C.L.E.
'''