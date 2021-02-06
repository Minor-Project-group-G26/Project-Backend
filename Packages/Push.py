import os
import pandas as pd
import sqlite3
class Make:

    def __init__(self):
        con = sqlite3.connect('project.db')
        self.movie = pd.read_sql_query('''SELECT * FROM Movie''', con).fillna(0)
        self.data = pd.read_sql_query(''' SELECT movie_id,movies_name,movies_poster,movie_rating FROM Data''', con).fillna(0)
        self.actors = pd.read_sql_query(''' SELECT * FROM Movie_Actor''', con)
        self.director = pd.read_sql_query(''' SELECT * FROM Movie_Director''', con)
        self.genres = pd.read_sql_query(''' SELECT * FROM Movie_Genres''', con)

    def deft(self, a1, a2, a3, a4, a5, a6, a7, a8, a9):
        data = {
            "Id": a1,
            "Poster": a2,
            "Title": a3,
            "Actor": a4,
            "Director": a5,
            "Category": a6,
            "Link": a7,
            "Blurb": a8,
            "Rate": a9
        }
        return data

    def MovieData(self, id):
        self.id = int(id)
        self.data.columns = ['Id', 'Title', 'Poster', 'Rate']
        return self.data.loc[self.data['Id'] == self.id].to_dict(orient='records')[0]

    def AllMovies(self, a, b):
        if a != None:
            self.data_id = self.movie['movie_id'].tolist()[a:b]
            self.all = list()
            for i in self.data_id:
                self.all.append(self.MovieData(id=i)[0])
            return self.all
        else:
            self.data_id = self.movie['movie_id'].tolist()
            self.all = list()
            for i in self.data_id:
                self.all.append(self.MovieData(id=i)[0])
            return self.all


# -------------------------------------------- End -------------------------------------------------------------------