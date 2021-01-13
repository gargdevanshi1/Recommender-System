# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:10:57 2019

@author: DEVANSHI GARG
"""


import pandas as pd
from ast import literal_eval
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

t_movies = pd.read_csv(r'/Users/devanshigarg/Desktop/RecommenderSystem/movies_metadata.csv', low_memory=False)

m = t_movies['vote_count'].quantile(0.85)
q_movies = t_movies.copy().loc[(t_movies['vote_count'] >= m)]
v = t_movies['vote_average'].mean()


def weightedRating(i, m=m, v=v):
    n = i['vote_count']
    r = i['vote_average']
    return ((n / (n + m)) * r + (m / (n + m)) * v)


q_movies['weighted_rating'] = q_movies.apply(weightedRating, axis=1)
q_movies = q_movies.sort_values('weighted_rating', ascending=False)

# would be required in content based Recommender System
credits = pd.read_csv(r'/Users/devanshigarg/Desktop/RecommenderSystem/credits.csv')
keywords = pd.read_csv(r'/Users/devanshigarg/Desktop/RecommenderSystem/keywords.csv')

credits['id'] = credits['id'].astype('int')
keywords['id'] = keywords['id'].astype('int')
q_movies['id'] = q_movies['id'].astype('int')

q_movies = q_movies.merge(credits, on='id')
q_movies = q_movies.merge(keywords, on='id')

def simpleRecommender():
    print('Is there a specific language you want?')
    a = input('Y/N\n')
    if a.lower() == 'n':
        print(q_movies[['title', 'original_language']].head(10))
    elif a.lower() == 'y':
        print("Choose Language")
        print('1) English')
        print('2) Hindi')
        print('3) French')
        print('4) Japanese')
        print('5) Others')
        b = int(input())
        if b == 1:
            lang = 'en'
        elif b == 2:
            lang = 'hi'
        elif b == 3:
            lang = 'fr'
        elif b == 4:
            lang = 'ja'
        else:
            lang = 'x'
        if lang != 'x':
            copy_movies = q_movies.copy().loc[q_movies['original_language'] == lang]
        else:
            copy_movies = q_movies.copy().loc[
                (q_movies['original_language'] != 'en') & (q_movies['original_language'] != 'hi') & (
                            q_movies['original_language'] != 'fr') & (q_movies['original_language'] != 'ja')]
        print(copy_movies[['title', 'original_language']].head(10))
        return


def getDirector(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan


def getList(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names
    return []


def modifyData(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''


def concatenateFeatures(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])


features = ['cast', 'crew', 'keywords', 'genres']

for feature in features:
    q_movies[feature] = q_movies[feature].apply(literal_eval)

q_movies['director'] = q_movies['crew'].apply(getDirector)

features = ['cast', 'genres', 'keywords']

for feature in features:
    q_movies[feature] = q_movies[feature].apply(getList)

features = ['cast', 'keywords', 'director', 'genres']

for feature in features:
    q_movies[feature] = q_movies[feature].apply(modifyData)

q_movies['combination'] = q_movies.apply(concatenateFeatures, axis=1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(q_movies['combination'])

cosine_sim = cosine_similarity(count_matrix, count_matrix)

q_movies = q_movies.reset_index()

indices = pd.Series(q_movies.index, index=q_movies['title']).drop_duplicates()


def contentBasedRecommender(title):
    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    movie_indices = [i[0] for i in sim_scores]

    print(q_movies['title'].iloc[movie_indices])
    return


while True:
    print('\nDo you want to enter a movie?')
    print('Y/N')
    a = input()
    while a.lower() != 'n' and a.lower() != 'y':
        print("\nEnter valid choice. \nY/N")
        a = input()
    else:
        if a.lower() == 'n':
            simpleRecommender()
        elif a.lower() == 'y':
            b = input('Enter movie name.\n')
            print('\n')
            try:
                contentBasedRecommender(b)
            except KeyError:
                print('Sorry, this movie cannot be found.')
    c = input('\nDo you want more recommendations? Y/N\n')
    if (c.lower() == 'y'):
        continue
    else:
        print('\nThanks for using our Recommender System.')
        break

