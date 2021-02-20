from flask import Flask, request, Response, render_template, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta
import json
import sqlite3

# Custom Packages And some Module Function(Global Functions)
# from Packages.User import User
from Packages.SqlDB import SqlDB
from Packages.modules import *
from Packages.AllRounder import Movies, Searching, FilterRecommend, Individual
from Packages.Movie import *
from Packages.Push import Make

# Routes handling
from Routes import Signin, Signup, ClientUser, CommentsRoute, ForgetSystem, AdminUser

app = Flask(__name__)
# Config upload files base path
app.config['UPLOAD_FOLDER'] = './static'

# Cross origin access config
CORS(app)

# Bcrypt config
bcrypt = Bcrypt(app)

#  load_dotenv with increased verbosity
load_dotenv(verbose=True)
# explicitly providing path to '.env'
env_path = Path('.') / ".env"

# Registering Blueprints for Routes
app.register_blueprint(Signup.construct_blueprint(bcrypt))
app.register_blueprint(Signin.construct_blueprint(bcrypt))
app.register_blueprint(ClientUser.construct_blueprint(app.config['UPLOAD_FOLDER']))
app.register_blueprint(AdminUser.construct_blueprint(app.config['UPLOAD_FOLDER']))
app.register_blueprint(CommentsRoute.construct_blueprint())
app.register_blueprint(ForgetSystem.construct_blueprint(bcrypt))


# ADMIN Route Handling

@app.route("/movie", methods=["POST", "GET"])
def saveDetails():
    if request.method == "POST":
        name = request.form["Name"]
        tp = request.form["Type"]
        cast = request.form["Cast"]
        dr = request.form["Dr"]
        b = request.form["Blurb"]
        link = request.form["Link"]
        f = request.files['Poster']
        poster = secure_filename(f.filename)
        f.save(os.path.join('./static/MoviePoster', poster))
        print(poster)
        movie = Movies()
        movie.Movies_Insert(mname=name, acname=cast, drname=dr, genname=tp, mblrb=b, mp=poster, ml=link)

    App = Movies()
    return Response(json.dumps(App.DisplayAll(1)), mimetype='application/json')

@app.route('/getstarted', methods=['GET'])
def getStarted():
    gtStart = Movies()
    return Response(json.dumps(gtStart.DisplayGetStarted()), mimetype='application/json')

@app.route('/categories', methods=['POST', 'GET'])
def setCat():
    if request.method == "POST":
        cat = request.form["Category"]
        category = Individual()
        res = category.Insert_Genres(cat)
        if res:
            return "Saved"
        return "fail"

    Geners = Movies()
    return Response(json.dumps(Geners.Full_Genres()), mimetype='application/json')


@app.route('/casts', methods=['POST', 'GET'])
def setCast():
    if request.method == "POST":
        cast = request.form["Name"]
        casts = Individual()
        res = casts.Insert_Actor(cast)
        if res:
            return "Saved"
        return "fail"

    Actors = Movies()
    return Response(json.dumps(Actors.Full_Actors()), mimetype='application/json')


@app.route('/directors', methods=['POST', 'GET'])
def setDr():
    if request.method == "POST":
        dr = request.form["Name"]
        drs = Individual()
        res = drs.Insert_Director(dr)
        if res:
            return "Saved"
        return "fail"

    Directors = Movies()
    return Response(json.dumps(Directors.Full_Directors()), mimetype='application/json')


@app.route('/movie/<mid>', methods=['GET'])
def GetOneMovie(mid):
    A = Movies()
    return Response(json.dumps(A.Movies_Edit_Display(a=mid)), mimetype='application/json')


@app.route('/movieuser/<mid>', methods=['GET'])
def GetNMovie(mid):
    A = Movies()
    return Response(json.dumps(A.Movies_Data_Display(a=mid)), mimetype='application/json')


@app.route('/home', methods=['GET', 'POST'])
def Home():
    if request.method == 'POST':
        token = request.form['token']
        if not VerifyToken(token=token, secret=os.getenv('SECRET_KEY')):
            return "invalid token"
        return "valid"


# ....................Get Image Route
@app.route('/get-file/<dest>/<file>', methods=['GET'])
def getFile(dest, file):
    # print(type,file)
    return send_from_directory(f"{app.config['UPLOAD_FOLDER']}/{dest}",
                               file)  # as_attachment=True to make it downloadable
    # return "file"


@app.route('/testupload', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        d = request.form['data']
        f = request.files['image']
        fileexe = secure_filename(f.filename).split('.')[-1]
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{d}.{fileexe}"))
        return 'file uploaded successfully'
    return render_template('home.html')


@app.route('/movieupdate', methods=['POST'])
def Update():
    m_id = request.form['Id']
    updated_name = request.form["Name"]
    updated_link = request.form["Link"]
    updated_type = request.form["Type"]
    updated_cast = request.form["Cast"]
    updated_director = request.form["Dr"]
    updated_blurb = request.form["Blurb"]
    f = request.files['Poster']

    updated_poster = secure_filename(f.filename)
    f.save(os.path.join('./static/MoviePoster', updated_poster))

    Object = Movies()
    Object.Movies_update(mid=m_id, mname=updated_name, drname=updated_director, acname=updated_cast,
                         genname=updated_type, ml=updated_link, mblrb=updated_blurb, mp=updated_poster)
    return "Done"


@app.route('/movie/search/<query>', methods=['GET'])
def SearchMovie(query):
    element = query
    element = element.lower()
    a = Searching()
    b = a.MoviesSearch(element)
    if len(b) != 0:
        return Response(json.dumps(b[:10]), mimetype='application/json')
    else:
        return ("No Data Found!!")


@app.route('/searchcat/<query>', methods=['GET'])
def SearchCat(query):
    element2 = query
    a = Searching()
    gen = a.GenresSearch(element2)
    if len(gen) != 0:
        return Response(json.dumps(gen[:10]), mimetype='application/json')
    else:
        return "Nothing Found"


@app.route('/categories/<query>', methods=['GET'])
def Cat(query):
    element2 = query
    a = Searching()
    gen = a.GenresSearch(element2)
    if len(gen) != 0:
        return Response(json.dumps(gen), mimetype='application/json')
    else:
        return "Nothing Found"


@app.route('/remove/<query>', methods=['GET'])
def RemoveMovie(query):
    Obj = Movies()
    Obj.Movies_delete(a=query)
    return "Successfully Deleted"


@app.route('/recom/<query>', methods=['GET'])
def recom(query):
    el = query
    data = FilterRecommend()
    newone = data.define_data(a=el)
    app1 = Searching()
    return Response(json.dumps(app1.CardManual(newone)), mimetype='application/json')


@app.route('/getcount/<count>', methods=['GET'])
def getCount(count):
    a = int(count)
    Ct = Movies()
    return Response(json.dumps(Ct.DisplayAll(a)), mimetype='application/json')


@app.route('/movie/searchall/<query>', methods=['GET'])
def SearchAll(query):
    Abc = Searching()
    return Response(json.dumps(Abc.Movies_DB_Search(query.lower())), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
