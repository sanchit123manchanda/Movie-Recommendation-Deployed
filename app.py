from flask import Flask, render_template, request, redirect
from predict_function import predict_movie
import pandas as pd

list_of_movies = pd.read_csv('ml-100k/u.item',sep = '\|',header = None)
list_of_movies = sorted(list(list_of_movies[1]))

def return_movies(movie):
    try:
        return predict_movie(movie)
    except:
        return ["MOVIE NOT FOUND! PLEASE TRY ANOTHER KEYWORD"]

app = Flask(__name__)

@app.route('/')
def start():
    return render_template("index.html",list_of_movies = list_of_movies)


@app.route('/submit',methods = ['POST'])

def submit():
    if request.method == 'POST':
        mov = request.form['mov']
        
        movies = return_movies(mov)
        if len(movies) == 0:
            movies = ["SORRY! NO SUGGESTIONS FOUND BASED ON THIS MOVIE"]
        elif len(movies) > 1:
            movies = list(movies.head(7).index)
        
    return (render_template("index.html",movies = movies,mov = mov))

if __name__ == '__main__':
    app.run(debug = True)