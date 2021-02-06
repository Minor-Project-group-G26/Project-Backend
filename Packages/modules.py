import os
from datetime import datetime

import jwt
from werkzeug.utils import secure_filename


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def fileUpload(file, allowed, destination, filename=''):
    ALLOWED_EXTENSIONS = allowed
    print(file, allowed, destination)
    try:
        if not filename:
            filename = secure_filename(file.filename)
        # print("start")
        if file and allowed_file(filename, ALLOWED_EXTENSIONS):
            print(filename)
            file.save(os.path.join(destination, filename))
            # print("uploaded")
            return filename
    except Exception as e:
        print('fail Error: ' + str(e))
        return False


def fileRemove(folder='', filename=''):
    try:
        for fname in os.listdir(folder):
            if fname.startswith(filename):
                os.remove(os.path.join(folder, fname))
                return True
        return False
    except Exception as e:
        print(e)
        return False


def ChnageToDict(**kwargs):
    NewDict = {}
    for key, value in kwargs.items():
        NewDict[key] = value
    return NewDict


# ......................... JWT Token Verifying
def VerifyToken(token, secret):
    token_data = jwt.decode(str(token), secret, algorithms=['HS256'])
    print(token_data)
    today = datetime.now().date()
    # expire = datetime.strptime(token_data['expire'], '%d/%m/%y %H:%M:%S.%f')
    # if expire < today:
    #     print("expired token")
    if token_data:
        return False
    return "Invalid Token"