import json
import os

import jwt
from flask import Blueprint, request, Response

from Packages.Comments import Comments
from Packages.modules import ChnageToDict, VerifyToken


def construct_blueprint():
    CommentsRoute = Blueprint("CommentsRoute", __name__)

    @CommentsRoute.route("/movies/<movieId>/comments", methods=['GET', 'POST'])
    def comments(movieId):
        MovieComments = Comments(movieId=movieId)
        if request.method == 'POST':
            if VerifyToken(token=request.form['token'], secret=os.getenv('SECRET_KEY')):
                return Response(json.dumps({"errors": "invalid token"}), mimetype='application/json', status=200)
            token_data = dict(jwt.decode(str(request.form['token']), os.getenv('SECRET_KEY'), algorithms=['HS256']))
            res = MovieComments.AddComments(comment=request.form['comment'], user_id=token_data['id'])
            if not res:
                return Response("Fail to Insert Comment")
            return Response("Inserted Comment")
        data = MovieComments.AllComments()
        print(data)
        DataDict = []
        for Id, username, userProfile, movie, comment, rating, doc in data:
            DataDict.append(ChnageToDict(id=Id, comment=comment, username=username, userProfile=userProfile, doc=doc,
                                         rating=round(rating, 1)))
        print(DataDict)
        return Response(json.dumps(DataDict), mimetype='application/json')

    @CommentsRoute.route('/movies/<movieId>/comments/<commentId>', methods=['GET', 'PUT', 'DELETE'])
    def UserComment(movieId, commentId):
        MovieComments = Comments(movieId=movieId)
        if request.method == 'PUT':
            if VerifyToken(token=request.form['token'], secret=os.getenv('SECRET_KEY')):
                return Response(json.dumps({"errors": "invalid token"}), mimetype='application/json', status=200)
            token_data = dict(jwt.decode(str(request.form['token']), os.getenv('SECRET_KEY'), algorithms=['HS256']))
            res = MovieComments.UserCommentUpdate(comment_id=commentId, user_id=token_data['id'],
                                                  comment=request.form['comment'])
            if not res:
                return "fail to Update"
            return "Success fully Update"

        if request.method == 'DELETE':
            if VerifyToken(token=request.form['token'], secret=os.getenv('SECRET_KEY')):
                return Response(json.dumps({"errors": "invalid token"}), mimetype='application/json', status=200)
            token_data = dict(jwt.decode(str(request.form['token']), os.getenv('SECRET_KEY'), algorithms=['HS256']))
            res = MovieComments.UserCommentDelete(comment_id=commentId, user_id=token_data['id'])
            if not res:
                return "Fail to delete"
            return "Deleted Successfully"

        data = MovieComments.SingleComments(comment_id=commentId)
        dataDict = ChnageToDict(id=data[0], comment=data[1], username=data[2], doc=data[3], rating=data[4])
        return dataDict

    @CommentsRoute.route('/movies/<movieId>/commentlist')
    def CommentList(movieId):
        MovieComments = Comments(movieId=movieId)
        resData = MovieComments.CommentList()
        return Response(json.dumps({"total": len(resData), "lastDate": resData[-1]}))

    return CommentsRoute

