# .............................................Sign Up Handler..........................................................
import json
import os
from datetime import datetime, timedelta

# from flask_bcrypt import Bcrypt
from flask import Blueprint, request, Response
import jwt
# ......................Custom Packages
from Packages.Admin import Admin
from Packages.User import User


def construct_blueprint(bcrypt):
    Signup = Blueprint("Signup", __name__)

    @Signup.route('/user/signup', methods=['POST'])
    def signup():
        if request.method == "POST":
            # Assign new user data
            newUser = User(name=request.form['name'], email=request.form['email'],
                           password=request.form['password'], phone=request.form['phone'])

            # checking if email or number exist
            existUser = newUser.SaveUser(bcrypt=bcrypt)
            print("is user")
            print(existUser)
            if existUser:
                return Response(json.dumps(existUser), mimetype='application/json', status=200)
            # Logging in after Saving data
            print("saved")
            savedUser = newUser.Login(bcrypt)

            print(savedUser)
            if savedUser:
                # Token Creating
                user_token = jwt.encode({'id': str(savedUser[0]), "email": str(savedUser[1]),
                                         "expire": str(datetime.now().date() + timedelta(7))}, os.getenv('SECRET_KEY'),
                                        algorithm='HS256')
                # print(user_token)
                return Response(json.dumps({"success": {"token": str(user_token), "name": str(savedUser[2])}}),
                                mimetype='application/json', status=200)
            return Response(json.dumps({"errors": {"error": "Something went wrong please try again later "}}),
                            mimetype='application/json', status=501)

    @Signup.route('/admin/signup', methods=['POST'])
    def SignUp():
        print("signup admin")
        admin = Admin(email=request.form['email'], password=request.form['password'], name=request.form['username']
                      , phone=request.form['phone'])
        res = admin.SaveUser(bcrypt)
        print(res)
        if res:
            return Response(response="Successful", status=200)
        return Response(response="fail to login", status=200)


    return Signup
