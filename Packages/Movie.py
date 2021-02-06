class Movie:
    def __init__(self, name='', poster='', link='', blrb=''):
        self._name = name
        self._poster = poster
        self._link = link
        self._blrb = blrb

    def Save(self, db):
        sql = 'INSERT into movies (movies_name, movies_link, movies_blurb, movies_poster) values ("%s","%s","%s", "%s")'% (self._name, self._link, self._blrb, self._poster)
        print(sql)
        if db.insertData(sql=sql):
           return True
        return False

    def Arrange(self,a):
        vss = []
        for val in a:
            vss.append(val["value"])
        return vss


# For Category Insertion
class Categorys:
    def __init__(self, category=''):
        self._category = category

    def CatSave(self, bd):
        sql = "INSERT into genres (genres_name) values ('%s')"% (self._category)
        print(sql)
        if bd.insertData(sql=sql):
           return True
        return False

# For Cast Insertion
class Casts:
    def __init__(self, cast=''):
        self._cast = cast

    def CastSave(self, ab):
        sql = "INSERT into actors (actor_name) values ('%s')"% (self._cast)
        print(sql)
        if ab.insertData(sql=sql):
           return True
        return False

# For Director Insertion
class Drs:
    def __init__(self, dr=''):
        self._dr = dr

    def DrSave(self, cd):
        sql = "INSERT into directors (director_name) values ('%s')"% (self._dr)
        print(sql)
        if cd.insertData(sql=sql):
           return True
        return False

