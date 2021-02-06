# ...........................................Sign in Route Handler......................................................
import json
import os
from datetime import datetime, timedelta

import jwt
from flask import Blueprint, request, Response
# ............Custom Packages
from Packages.Admin import Admin
from Packages.User import User


# ................Constructor to get arguments
def construct_blueprint(bcrypt):
    Signin = Blueprint("Signin", __name__)

    @Signin.route('/user/signin', methods=['POST'])
    def signin():

        # Login object
        user = User(email=request.form['email'], password=request.form['password'])
        # checking, is data is correct
        Userdata = user.Login(bcrypt=bcrypt)
        print(Userdata[0])
        if not Userdata:
            return Response(json.dumps({"errors": {"email": "please check wrong email or password"}}),
                                mimetype="application/json", status=200)
            # Token Creating
        user_token = jwt.encode({'id': str(Userdata[0]), "email": str(Userdata[1]),
                                "expire": str(datetime.now().date() + timedelta(7))}, os.getenv('SECRET_KEY'),
                                algorithm='HS256')
        return Response(json.dumps({"success": {"token": str(user_token), "name": str(Userdata[2])}}),
                        mimetype='application/json', status=200)


    @Signin.route('/admin/signin', methods=['POST'])
    def Login():
        admin = Admin(email=request.form['email'], password=request.form['password'])
        Admindata = admin.Login(bcrypt)
        if not admin:
            return Response(json.dumps({"errors": {"email": "please check wrong email or password"}}),
                            mimetype="application/json", status=200)
            # Token Creating
        print("Admin Data :", Admindata)
        admin_token = jwt.encode({'id': str(Admindata[0]), "email": str(Admindata[1]),
                                  "expire": str(datetime.now().date() + timedelta(7))}, os.getenv('SECRET_KEY'),
                                 algorithm='HS256')
        print("Token  48 :", admin_token)

        return Response(json.dumps({"success": {"token": str(admin_token), "name": str(Admindata[2])}}),
                        mimetype='application/json', status=200)

    return Signin
