import pandas as pd
import sqlite3


class Searching:
    def __init__(self):
        connection = sqlite3.connect('project.db')
        self.movies = pd.read_sql_query("SELECT movie_id,movies_name,movies_poster,movie_rating FROM Data",connection)
        self.movie = pd.read_sql_query("SELECT movie_id,genres_name FROM movies", connection)

    def Manage(self, a, b, c, d):
        if d != None:
            dart = {
                "Id": a,
                "Title": b,
                "Poster": c,
                "Rate": round(d,1)
            }
        else:
            dart = {
                "Id": a,
                "Title": b,
                "Poster": c,
                "Rate": 0
            }
        return dart


    def SearchData(self, search):
        a = self.movie.loc[self.movie.genres_name.str.contains(search, na=False)].movie_id.values.tolist()
        condition_genres = self.movies.movie_id.isin(a)
        condition = (self.movies.movies_name.str.contains(search, na=False)) | condition_genres
        self.Mdata = self.movies.loc[condition]
        self.Wdata = []
        for i, j, k, l in self.Mdata.values.tolist():
            self.Wdata.append(self.Manage(i, j, k, l))
        return self.Wdata

    def SearchCat(self, search):
        a = self.movie.loc[self.movie.genres_name.str.contains(search, na=False)].movie_id.values.tolist()
        z = self.movies.movie_id.isin(a)
        self.gen = self.movies.loc[z]
        self.bag = []
        # print(self.gen.columns)
        self.gen['movie_rating'].fillna(0)
        for i, j, k, l in self.gen.values.tolist():
            self.bag.append(self.Manage(i, j, k, l))
        return self.bag


if __name__ == '__main__':
    A = Minor()
    print(A.SearchCat(search='Comedies'))
