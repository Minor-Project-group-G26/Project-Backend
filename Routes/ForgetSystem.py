import json
import os
from datetime import datetime, timedelta

import jwt
from flask import Blueprint, request, Response

from Packages.Admin import Admin
from Packages.User import User


def construct_blueprint(bcrypt):
    ForgetSystem = Blueprint("ForgetSystem", __name__)

    @ForgetSystem.route("/user/forget", methods=["PUT"])
    def ForgetPassword():
        user = User(email=request.form['email'], phone=request.form['phone'])
        Id = user.ForgetPassword()
        if Id:
            Ftoken = jwt.encode({'id': Id}, os.getenv('SECRET_KEY'), algorithm='HS256')
            return Response(json.dumps({"success": Ftoken}), mimetype="application/json")
        return Response(json.dumps({"errors": "Wrong Email or Phone"}), mimetype="application/json")
        # return "success"

    @ForgetSystem.route("/user/reset", methods=["PUT"])
    def Reset():
        token_data = dict(jwt.decode(str(request.form['tokenId']), os.getenv('SECRET_KEY'), algorithms=['HS256']))
        print(token_data)
        user = User(Id=token_data['id'])
        print(user)
        res = user.NewPassword(bcrypt, request.form['newPassword'])
        return Response(json.dumps({"result": res}), mimetype="application/json")

    @ForgetSystem.route("/admin/forget", methods=["PUT"])
    def AdminForgetPassword():

        user = Admin(email=request.form['email'], phone=request.form['phone'])
        Id = user.ForgetPassword()
        print(Id)
        # return "Working"
        if Id:
            Ftoken = jwt.encode({'id': Id}, os.getenv('SECRET_KEY'), algorithm='HS256')
            return Response(json.dumps({"success": Ftoken}), mimetype="application/json")
        return Response(json.dumps({"errors": "Wrong Email or Phone"}), mimetype="application/json")

    @ForgetSystem.route("/admin/reset", methods=["PUT"])
    def AdminReset():
        token_data = dict(jwt.decode(str(request.form['tokenId']), os.getenv('SECRET_KEY'), algorithms=['HS256']))
        print(token_data)
        user = Admin(Id=token_data['id'])
        print(user)
        res = user.NewPassword(bcrypt, request.form['newPassword'])
        return Response(json.dumps({"result": res}), mimetype="application/json")

    return ForgetSystem