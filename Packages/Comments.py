import os

from textblob import TextBlob

from Packages.SqlDB import SqlDB


class Comments(SqlDB):
    def __init__(self, movieId=''):
        super().__init__(filename=os.getenv('DB_FILE'))
        self._movieId = movieId

    def AllComments(self):
        # sql = f"""Select * from comments join movies on comments.movie_id = movie.id  where
        # comments.movie_id = {self._movieId}"""
        data = super().getData(f"""select * from CommentList where movie_id= {self._movieId} order by DOU desc""")
        print(data)
        return data

    def UserComments(self, user_id=''):
        data = super().getData(f"""select id, comment, user_id, DOC FROM comments where movie_id = {self._movieId} 
                            and user_id ={user_id}""")
        print(data)
        return data

    def SingleComments(self, comment_id=''):
        data = super().GetDataAdvance(table='comments', FindKey={"movie_id": self._movieId, "id": comment_id},
                                      connection={}, get=['id', 'comment', 'user_id', 'DOC', 'rating'])
        # , f"""select id, comment, user_id, DOC FROM comments where movie_id = {self._movieId}
        #                             and id={comment_id}"""
        print(data)
        return data

    def AddComments(self, user_id, comment=''):
        bob = TextBlob(comment)
        rating = (bob.sentiment.polarity + bob.sentiment.subjectivity) / 2
        if rating < 0.1:
            rating = 0.10
        if rating > 1.0:
            rating = 1.0
        print(rating)
        data = super().InsertDataAdvance(table='comments', movie_id=self._movieId, user_id=user_id, comment=comment,
                                         rating=str(rating * 10), DOC=True, DOU=True)
        print(data)
        return data

    def UserCommentUpdate(self, comment_id, user_id, comment):
        bob = TextBlob(comment)
        rating = (bob.sentiment.polarity + bob.sentiment.subjectivity) / 2
        print(rating)
        res = super().UpdateDataAdvance(table="comments",
                                        FindKey={"id": comment_id, "movie_id": self._movieId, "user_id": user_id},
                                        comment=comment, rating=str(rating * 10), DOU=True)
        print(res)
        return res

    def UserCommentDelete(self, comment_id, user_id):
        res = super().DeleteDataAdvance(table="comments",
                                        FindKey={"id": comment_id, "movie_id": self._movieId, "user_id": user_id})
        print(res)
        return res

    def CommentList(self):
        res = super().GetDataAdvance(table="CommentList", FindKey={"movie_id": self._movieId},
                                     get=['DOU'])
        print(res)
        return res

    def __del__(self):
        super().Close()
