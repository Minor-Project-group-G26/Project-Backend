import pandas as pd
import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ------------------------------------------ Movies Class ----------------------------------------------------------#
class Movies:
    def __init__(self):
        self.db = sqlite3.connect('project.db')
        self.movies_table = pd.read_sql_query("SELECT * FROM movies", self.db)
        self.movies_table2 = pd.read_sql_query("SELECT * FROM movies", self.db)
        self.movies_genres_table = pd.read_sql_query("SELECT * FROM movies_genres", self.db)
        self.movies_actors_table = pd.read_sql_query("SELECT * FROM movies_actors", self.db)
        self.movies_directors_table = pd.read_sql_query("SELECT * FROM movies_directors", self.db)
        self.actors_table = pd.read_sql_query("SELECT * FROM actors", self.db)
        self.genres_table = pd.read_sql_query("SELECT * FROM genres", self.db)
        self.directors_table = pd.read_sql_query("SELECT * FROM directors", self.db)
        self.rating_data = pd.read_sql_query("SELECT movie_id, movie_rating FROM Data", self.db)
        self.rating_data.movie_rating.fillna(0, inplace=True)
        self.movies_searching = pd.read_sql_query("SELECT movie_id,movies_name,movies_poster,movie_rating FROM Data",self.db)
        self.genre_searching = pd.read_sql_query("SELECT movie_id,genres_name FROM movies", self.db)
        self.boss = self.movies_table
        self.boss['movies_name'] = self.boss['movies_name'].str.lower()

    # ------------------------- Method to Convert a list into String -------------------------------------------------#
    def array_to_str(self, a):
        d = 0
        string = ""
        for i in a:
            if d != 0:
                string = string + "," + i
                d = d + 1
            else:
                string = i
                d = d + 1
        return string

    def str_to_array(self, b):
        return b.split(',')
    # ---------------------------------- Fetching Name Methods ------------------------------------------------------#
    def acr_name(self, a):
        ac_name = []
        for i in a:
            i =int(i)
            ac_name.append(self.actors_table.loc[self.actors_table.actors_id == i].actor_name.values.tolist()[0])
        self.actors_name = self.array_to_str(ac_name)
        return self.actors_name

    def dir_name(self, a):
        dr_name = []
        for i in a:
            i = int(i)
            dr_name.append(self.directors_table.loc[self.directors_table.directors_id == i].director_name.values.tolist()[0])
        self.directors_name = self.array_to_str(dr_name)
        return self.directors_name

    def genr_name(self, a):
        gn_name = []
        for i in a:
            i = int(i)
            gn_name.append(self.genres_table.loc[self.genres_table.genres_id == i].genres_name.values.tolist()[0])
        self.genres_name = self.array_to_str(gn_name)
        return self.genres_name

    # --------------------------------------- Inserting Singly -------------------------------------------------------#
    def Actors_Insert(self, a, b):
        cur = self.db.cursor()
        sql1 = "INSERT INTO movies_actors(movie_id, actors_id) VALUES (?,?)"
        for i in a:
            cur.execute(sql1, (b, i))
            self.db.commit()

    def Directors_Insert(self, a, b):
        cur = self.db.cursor()
        sql1 = "INSERT INTO movies_directors(movie_id, directors_id) VALUES (?,?)"
        for i in a:
            cur.execute(sql1, (b, i))
            self.db.commit()

    def Genres_Insert(self, a, b):
        cur = self.db.cursor()
        sql1 = "INSERT INTO movies_genres(movie_id, genres_id) VALUES (?,?)"
        for i in a:
            cur.execute(sql1, (b, i))
            self.db.commit()

    # ---------------------------------------- Deleting Singly -------------------------------------------------------#
    def Actors_Delete(self, a):
        cur = self.db.cursor()
        sql = " DELETE FROM movies_actors WHERE movie_id = ? "
        cur.execute(sql, (a,))
        self.db.commit()

    def Directors_Delete(self, a):
        cur = self.db.cursor()
        sql = " DELETE FROM movies_directors WHERE movie_id = ? "
        cur.execute(sql, (a,))
        self.db.commit()

    def Genres_Delete(self, a):
        cur = self.db.cursor()
        sql = " DELETE FROM movies_genres WHERE movie_id = ? "
        cur.execute(sql, (a,))
        self.db.commit()

    # ------------------------------------------------- Updating Singly ----------------------------------------------#
    def Genres_Update(self, a, b):
        self.Genres_Delete(b)
        self.Genres_Insert(a, b)

    def Actors_Update(self, a, b):
        self.Actors_Delete(b)
        self.Actors_Insert(a, b)

    def Directors_Update(self, a, b):
        self.Directors_Delete(b)
        self.Directors_Insert(a, b)

    # ================================================ Movie's Updating ==============================================#
    def Movies_update(self, mid, mname, drname, acname, genname, mblrb, mp, ml):
        mid = int(mid)
        self.acname_update = self.str_to_array(acname)
        self.drname_update = self.str_to_array(drname)
        self.genname_update = self.str_to_array(genname)
        m = [mid, mname, self.dir_name(self.drname_update), self.acr_name(self.acname_update), self.genr_name(self.genname_update), mblrb, mp, ml]
        self.movies_table.loc[
            self.movies_table.movie_id == mid, ['movie_id', 'movies_name', 'directors_name', 'actors_name',
                                                'genres_name', 'movies_blurb', 'movies_poster', 'movies_link']] = m
        self.movies_table.to_sql(name="movies", con=self.db, index=False, if_exists="replace")
        self.Genres_Update(self.genname_update, mid)
        self.Actors_Update(self.acname_update, mid)
        self.Directors_Update(self.drname_update, mid)

    # =========================================== Movie's Insertion ==================================================#
    def Movies_Insert(self, mname, acname, drname, genname, mblrb, mp, ml):
        self.acname_insert = self.str_to_array(acname)
        self.drname_insert = self.str_to_array(drname)
        self.genname_insert = self.str_to_array(genname)
        self.a = self.movies_table.index.stop + 1
        print(mname,self.acname_insert, self.drname_insert, self.genname_insert, mblrb, mp, ml)
        mb = [int(self.a), mname, self.dir_name(self.drname_insert), self.acr_name(self.acname_insert),
              self.genr_name(self.genname_insert), mblrb, mp, ml]
        print(mb)
        self.movies_table.loc[
            int(self.a), ['movie_id', 'movies_name', 'directors_name', 'actors_name',
                          'genres_name', 'movies_blurb', 'movies_poster', 'movies_link']] = mb

        self.movies_table['movie_id'] = self.movies_table.movie_id.astype(int)
        self.movies_table = self.movies_table
        self.movies_table.to_sql(name="movies", con=self.db, index=False, if_exists="replace")
        print(genname)
        self.Genres_Insert(self.genname_insert, self.a)
        print(acname)
        self.Actors_Insert(self.acname_insert, self.a)
        print(drname)
        self.Directors_Insert(self.drname_insert, self.a)

    # ========================================== Movie's Deletion =================================================== #
    def Movies_delete(self, a):
        cur = self.db.cursor()
        sql = " DELETE FROM movies WHERE movie_id = ? "
        cur.execute(sql, (a,))
        self.db.commit()
        self.Actors_Delete(a)
        self.Directors_Delete(a)
        self.Genres_Delete(a)
        return "Deleted"
    # ------------------------------------------- Dispaly ----------------------------------------------------------#

    def DisplayOne(self, a):

        return self.movies_table.loc[self.movies_table.movie_id == a].to_dict(orient='records')

    def DisplayAll(self, a):
        page_number = self.movies_table.index.stop
        rem = page_number % 10
        if a > ((page_number - rem) // 10) + 1:
            a = (page_number - rem) // 10
        self.movies_table.columns = ['Id','Title','Director','Actor','Category','Blurb','Poster','Link']
        print(self.movies_table.to_dict(orient="records")[(a - 1) * 10: a * 10])
        return self.movies_table.to_dict(orient="records")[(a - 1) * 10: a * 10]

    def Movies_Data_Display(self, a):
        a = int(a)
        z = self.movies_actors_table.loc[self.movies_actors_table.movie_id == a].actors_id.to_list()
        x = self.movies_directors_table.loc[self.movies_directors_table.movie_id == a].directors_id.to_list()
        y = self.movies_genres_table.loc[self.movies_genres_table.movie_id == a].genres_id.to_list()
        z1 = self.acr_name(a=z).split(",")
        x1 = self.dir_name(a=x).split(",")
        y1 = self.genr_name(a=y).split(",")
        return {
            "id": self.movies_table.loc[self.movies_table.movie_id == a].movie_id.tolist()[0],
            "Title": self.movies_table.loc[self.movies_table.movie_id == a].movies_name.tolist()[0],
            "Blurb": self.movies_table.loc[self.movies_table.movie_id == a].movies_blurb.tolist()[0],
            "Poster": self.movies_table.loc[self.movies_table.movie_id == a].movies_poster.tolist()[0],
            "Link": self.movies_table.loc[self.movies_table.movie_id == a].movies_link.tolist()[0],
            "Actor": z1,
            "Director": x1,
            "Category": y1,
            "Rate": self.rating_data.loc[self.rating_data.movie_id == a].movie_rating.round(1).tolist()[0]
        }

    def DisplayGetStarted(self):
        getStarted = list()
        for i in range(12):
            getStarted.append(self.Movies_Data_Display(i))
        return getStarted

    def Movies_Edit_Display(self, a):
        a = int(a)
        z = self.movies_actors_table.loc[self.movies_actors_table.movie_id == a].actors_id.to_list()
        x = self.movies_directors_table.loc[self.movies_directors_table.movie_id == a].directors_id.to_list()
        y = self.movies_genres_table.loc[self.movies_genres_table.movie_id == a].genres_id.to_list()
        z1 = self.acr_name(a=z).split(",")
        x1 = self.dir_name(a=x).split(",")
        y1 = self.genr_name(a=y).split(",")
        return {
            "id": self.movies_table.loc[self.movies_table.movie_id == a].movie_id.tolist()[0],
            "Title": self.movies_table.loc[self.movies_table.movie_id == a].movies_name.tolist()[0],
            "Blurb": self.movies_table.loc[self.movies_table.movie_id == a].movies_blurb.tolist()[0],
            "Poster": self.movies_table.loc[self.movies_table.movie_id == a].movies_poster.tolist()[0],
            "Link": self.movies_table.loc[self.movies_table.movie_id == a].movies_link.tolist()[0],
            "Actor": z1,
            "Director": x1,
            "Category": y1
        }

    def Full_Actors(self):
        self.full_actors = self.actors_table
        self.full_actors.columns = ['value', 'label']
        return self.full_actors.to_dict(orient='records')

    def Full_Genres(self):
        self.full_genres = self.genres_table
        self.full_genres.columns = ['value', 'label']
        return self.full_genres.to_dict(orient='records')

    def Full_Directors(self):
        self.full_directors = self.directors_table
        self.full_directors.columns = ['value','label']
        return self.full_directors.to_dict(orient='records')

    #-----------------------------------------------Working------------------------------------------------------------#

class FilterRecommend(Movies):

    def get_title_from_index(self, index):
        return self.movies_table[self.movies_table.movie_id == index]["movies_name"].values[0]

    def get_index_from_title(self, title):
        return self.movies_table[self.movies_table.movies_name == title]["movie_id"].values[0]

    def combine_features(self, row):
        try:
            return row['movies_name'] + " " + row['actors_name'] + " " + row['genres_name'] + " " + row[
                'directors_name'] + " " + row['movies_blurb']
        except:
            pass

    def define_data(self, a):
        __features = ['movies_name', 'actors_name', 'genres_name', 'directors_name', 'movies_blurb']

        for feature in __features:
            self.movies_table[feature] = self.movies_table[feature].fillna('')
            self.movies_table["combined_features"] = self.movies_table.apply(self.combine_features, axis=1)
        __cv = CountVectorizer()
        __count_matrix = __cv.fit_transform(self.movies_table["combined_features"])
        __cosine_sim = cosine_similarity(__count_matrix)
        __movie_user_likes = a
        __movie_index = self.get_index_from_title(__movie_user_likes)
        __similar_movies = list(enumerate(__cosine_sim[__movie_index]))
        __sorted_similar_movies = sorted(__similar_movies, key=lambda x: x[1], reverse=True)
        __get_data = list()
        i = 0
        for element in __sorted_similar_movies:
            __get_data.append(element[0])
            i = i + 1
            if i > 8:
                break
        return __get_data

    def Get_Recommendation(self, a):
        self.icons = self.define_data(a)
        cp = self.movies_table.movie_id.isin(self.icons)
        # print(self.movies_table.loc[cp].drop('combined_features', axis=1).to_dict(orient='records'))
        return self.movies_table.loc[cp].drop('combined_features', axis=1).to_dict(orient='records')


# ------------------------------------------ Searching ---------------------------------------------------------------#

class Searching(Movies):

    def MoviesSearch(self, ab):
        self.boss = self.movies_table
        self.boss['movies_name'] = self.boss['movies_name'].str.lower()
        a = self.movies_searching.loc[self.boss.movies_name.str.contains(ab)].movie_id.values.tolist()
        condition = self.movies_searching.movie_id.isin(a)
        self.movies_searching.columns = ['Id', 'Title', 'Poster', 'Rate']
        apple = self.movies_searching.loc[condition]
        apple.fillna(0, inplace=True)
        apple.Rate = apple.Rate.round(1)
        return apple.to_dict(orient='records')

    def GenresSearch(self, ab):
        a = self.genre_searching.loc[self.genre_searching.genres_name.str.contains(ab, na=False)].movie_id.values.tolist()
        z = self.movies_searching.movie_id.isin(a)
        self.movies_searching.columns = ['Id', 'Title', 'Poster', 'Rate']
        apple1 = self.movies_searching.loc[z]
        apple1.fillna(0, inplace=True)
        apple1.Rate = apple1.Rate.round(1)
        return apple1.to_dict(orient='records')

    def CardManual(self, card):
        condition = self.movies_searching.movie_id.isin(card)
        self.movies_searching.columns = ['Id', 'Title', 'Poster', 'Rate']
        apple = self.movies_searching.loc[condition]
        apple.fillna(0, inplace=True)
        apple.Rate = apple.Rate.round(1)
        return apple.to_dict(orient='records')

    def Movies_DB_Search(self, ab):
        a = self.boss.loc[self.boss.movies_name.str.contains(ab)].movie_id.values.tolist()
        condition = self.movies_table2.movie_id.isin(a)
        self.movies_table2.columns = ['Id', 'Title', 'Director', 'Actor', 'Category', 'Blurb', 'Poster', 'Link']
        print(self.movies_table2.loc[condition].to_dict(orient='records'))
        return self.movies_table2.loc[condition].to_dict(orient='records')

#-----------------------------------------Individual-----------------------------------------------------------#

class Individual:
    def __init__(self):
        self.connection = sqlite3.connect('project.db')
        self.actors = pd.read_sql_query("SELECT * FROM actors", self.connection)
        self.genre = pd.read_sql_query("SELECT * FROM genres", self.connection)
        self.director = pd.read_sql("SELECT * FROM directors", self.connection)

    def Insert_Actor(self, actor):
        if type('str') == type(actor):
            a1 = self.actors.index.stop + 1
            sql = f" INSERT INTO actors(actors_id, actor_name) VALUES({a1},'{actor}')"
            cur = self.connection.cursor()
            cur.execute(sql)
            self.connection.commit()
            return True
        else:
            return False

    def Insert_Director(self, director):
        if type('str') == type(director):
            a2 = self.director.index.stop + 1
            sql1 = f" INSERT INTO directors(directors_id, director_name) VALUES({a2},'{director}')"
            cur = self.connection.cursor()
            cur.execute(sql1)
            self.connection.commit()
            return True
        else:
            return False

    def Insert_Genres(self, genres):
        if type('str') == type(genres):
            a3 = self.genre.index.stop + 1
            sql = f" INSERT INTO genres(genres_id, genres_name) VALUES({a3},'{genres}')"
            cur = self.connection.cursor()
            cur.execute(sql)
            self.connection.commit()
            return True
        else:
            return False
