import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

columns_names = ['user_id','item_id','rating','timestamp']
df = pd.read_csv('ml-100k/u.data',sep = '\t',names = columns_names)

movies_title = pd.read_csv('ml-100k/u.item',sep = '\|',header = None)


movies_title = movies_title[[0,1]]
movies_title.columns  = ['item_id','title']

df = pd.merge(df,movies_title,on = 'item_id')

ratings = pd.DataFrame(df.groupby('title').mean()['rating'])
ratings['num of ratings'] = pd.DataFrame(df.groupby('title').count()['rating'])

moviesmat = df.pivot_table(index = 'user_id',columns = 'title',values = 'rating')


def predict_movie(movie_name):
    movie_user_ratings = moviesmat[movie_name]
    similar_to_movie = moviesmat.corrwith(movie_user_ratings)
    
    corr_movie = pd.DataFrame(similar_to_movie,columns = ['Correlation'])
    corr_movie.dropna(inplace = True)
    corr_movie = corr_movie.join(ratings['num of ratings'])
    
    pred = corr_movie[corr_movie['num of ratings']> 100].sort_values('Correlation',ascending = False)
    return pred[1:]

if __name__ == '__main__':
    
    mv = input("Select Your Favorite Movie: ")
    
    predicted_movies = predict_movie(mv)
    
    print("Movies Recommended for you are: \n")
    for movie in predicted_movies.head(7).index:
        print(movie)

