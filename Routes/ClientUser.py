# .........................................Client-Side Router...........................................................

import json
import os
from datetime import datetime
from flask import Blueprint, request, Response
import jwt
from werkzeug.utils import secure_filename

# Custom Packages And some Module Function(Global Functions)
from Packages.Admin import Admin
from Packages.User import User
from Packages.modules import fileUpload, fileRemove, VerifyToken


# ...........Constructor for getting arguments
def construct_blueprint(uploadFolder):
    ClientUser = Blueprint("User", __name__)

    @ClientUser.route('/user/profile/<UserToken>', methods=['GET', 'PUT'])
    def Profile(UserToken):
        tokenError = VerifyToken(token=UserToken, secret=os.getenv('SECRET_KEY'))
        if tokenError:
            return Response(json.dumps({"error": {"text": tokenError, "token": False}}),
                            mimetype='application/json', status=200)
        token_data = dict(jwt.decode(str(UserToken), os.getenv('SECRET_KEY'), algorithms=['HS256']))
        user = User(Id=token_data['id'])
        # PUT
        if request.method == 'PUT':

            # # ...............Profile Image Handler
            filename = ""
            try:
                file = request.files['profileImage']
                fileRemove(folder=f"{uploadFolder}/users", filename=request.form['email'])
                # print(file)
                # ................... Profile Image
                today = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                filename = f"""{request.form['email']}{today}.{secure_filename(file.filename).split('.')[-1]}"""
                filename = fileUpload(file=file, destination=f"{uploadFolder}/users",
                                      allowed={'png', 'jpg', 'jpeg'}, filename=filename)
            except Exception as e:
                print("No file received "+str(e))

            # ...........................Profile data Handler
            try:
                print(filename, "filename")
                err = user.UpdateData(username=request.form['name'], phone=request.form['phone'], profileImage=filename)
                print(err)
                if err:
                    return Response(json.dumps({"errorPhone": f"fail to update {err}"}), mimetype='application/json',
                                    status=200)
                return Response(json.dumps({"success": "successfully updated "}), mimetype='application/json',
                                status=200)
            except Exception as e:
                print(e)
                return Response(json.dumps({"error": {"text": f"fail to update"}}), mimetype='application/json',
                                status=200)

        # .......................... GET
        UserData = user.FetchData()
        return Response(json.dumps(UserData), mimetype='application/json', status=200)

    # ............Plan Route
    @ClientUser.route('/plan', methods=['PUT'])
    def Plan():
        if VerifyToken(token=request.form['token'], secret=os.getenv('SECRET_KEY')):
            return Response(json.dumps({"errors": "invalid token"}), mimetype='application/json', status=200)
        token_data = dict(jwt.decode(str(request.form['token']), os.getenv('SECRET_KEY'), algorithms=['HS256']))
        user = User(Id=token_data['id'])
        err = user.UpdatePlan(plantype=request.form['plantype'])
        if err:
            return Response(json.dumps({"errors": f"fail to update {err}"}), mimetype='application/json', status=200)
        return Response(json.dumps({"success": "successfully activated "}), mimetype='application/json', status=200)

    @ClientUser.route('/users/is/<Id>/<great>',methods=['GET'])
    def SingleUser(Id, great):
        user = User(Id=Id)
        res = user.NextUser(great)
        print(res)

        return Response(json.dumps({"success": res}), mimetype='application/json', status=200)

    @ClientUser.route("/users/verify/plan/<token>", methods=['GET'])
    def PlanVerify(token):
        if VerifyToken(token=token, secret=os.getenv('SECRET_KEY')):
            return Response(json.dumps({"errors": "invalid token"}), mimetype='application/json', status=200)
        token_data = dict(jwt.decode(str(token), os.getenv('SECRET_KEY'), algorithms=['HS256']))
        user = User(Id=token_data['id'])
        res = user.PlanValid()
        print(res)
        return Response(json.dumps({"planActive": res}), mimetype="application/json")


    return ClientUser
