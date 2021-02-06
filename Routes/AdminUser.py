# .........................................Client-Side Router...........................................................

import json
import os
from datetime import datetime
from flask import Blueprint, request, Response
import jwt
from werkzeug.utils import secure_filename

# Custom Packages And some Module Function(Global Functions)
from Packages.modules import fileUpload, fileRemove, VerifyToken
from Packages.Admin import Admin


# ...........Constructor for getting arguments
def construct_blueprint(uploadFolder):
    AdminUser = Blueprint("Admin", __name__)

    # .........................Admin Side

    @AdminUser.route("/users/<token>/<ID>/<great>", methods=["GET", "DELETE"])
    def AllUser(token, ID, great):

        tokenError = VerifyToken(token=token, secret=os.getenv('SECRET_KEY'))
        if tokenError:
            return Response(json.dumps({"error": {"text": tokenError, "token": False}}),
                            mimetype='application/json', status=200)

        token_data = dict(jwt.decode(str(token), os.getenv('SECRET_KEY'), algorithms=['HS256']))
        admin = Admin(Id=token_data['id'])

        if request.method == "DELETE":
            print(fileRemove(folder=f"{uploadFolder}/users", filename=request.form['email']))
            print(request.form['id'])
            res =admin.DeleteUser(user_id=request.form['id'])
            return Response(response=json.dumps({"success":res, "users": admin.AllUsers(ID, great)}),
                            mimetype='application/json')

        allUsers = admin.AllUsers(Id=ID, great=great)


        return Response(response=json.dumps(allUsers), mimetype="application/json", status=200)

    return AdminUser
