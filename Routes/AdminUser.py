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

    @AdminUser.route("/users/<token>/<Page>", methods=["GET", "DELETE"])
    def AllUser(token, Page):

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
            return Response(response=json.dumps({"success": res}),
                            mimetype='application/json')

        allUsers = admin.AllUsers(page=int(Page))
        return Response(response=json.dumps(allUsers), mimetype="application/json", status=200)

    @AdminUser.route("/users/<token>/<Page>/<search>", methods=["GET"])
    def SearchUser(token, Page, search):

        tokenError = VerifyToken(token=token, secret=os.getenv('SECRET_KEY'))
        if tokenError:
            return Response(json.dumps({"error": {"text": tokenError, "token": False}}),
                            mimetype='application/json', status=200)

        token_data = dict(jwt.decode(str(token), os.getenv('SECRET_KEY'), algorithms=['HS256']))
        admin = Admin(Id=token_data['id'])
        allUsers = admin.AllUsers(page=int(Page), Search=search)
        return Response(response=json.dumps(allUsers), mimetype="application/json", status=200)

    @AdminUser.route("/admin/profile/<token>", methods=['GET', 'PUT'])
    def Profile(token):
        tokenError = VerifyToken(token=token, secret=os.getenv('SECRET_KEY'))
        if tokenError:
            return Response(json.dumps({"error": {"text": tokenError, "token": False}}),
                            mimetype='application/json', status=200)
        token_data = dict(jwt.decode(str(token), os.getenv('SECRET_KEY'), algorithms=['HS256']))
        admin = Admin(Id=token_data['id'])
        # PUT
        if request.method == 'PUT':

            # # ...............Profile Image Handler
            filename = ""
            try:
                file = request.files['profileImage']
                fileRemove(folder=f"{uploadFolder}/admin", filename=request.form['email'])
                # print(file)
                # ................... Profile Image
                today = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                filename = f"""{request.form['email']}{today}.{secure_filename(file.filename).split('.')[-1]}"""
                filename = fileUpload(file=file, destination=f"{uploadFolder}/users",
                                      allowed={'png', 'jpg', 'jpeg'}, filename=filename)
            except Exception as e:
                print("No file received " + str(e))

                # ...........................Profile data Handler
            try:
                print(filename, "filename")
                err = admin.UpdateData(username=request.form['name'], phone=request.form['phone'],
                                       profileImage=filename)
                print(err)
                if err:
                    return Response(json.dumps({"errorPhone": f"fail to update {err}"}),
                                    mimetype='application/json',
                                    status=200)
                return Response(json.dumps({"success": "successfully updated "}), mimetype='application/json',
                                status=200)
            except Exception as e:
                print(e)
                return Response(json.dumps({"error": {"text": f"fail to update"}}), mimetype='application/json',
                                status=200)

            # .......................... GET
        AdminData = admin.FetchData()
        return Response(json.dumps(AdminData), mimetype='application/json', status=200)


    return AdminUser
