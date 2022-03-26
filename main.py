from flask import Flask, render_template, request, flash, redirect
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/task2"
mongo = PyMongo(app)


@app.route("/")
def home_page():
    online_users = mongo.db.users.find({})
    return render_template("list.html", users=online_users)

@app.route("/signup")
def enregistrer():
    return render_template("SignUp.html")


@app.route('/auth')
def auth():
    return render_template("authentification.html")

#SignUp
@app.route('/sign', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("form.html")
    else:
        lname = request.form.get("fname")
        fname = request.form.get("lname")
        mongo.db.user.insert_one({"username":lname,"password":generate_password_hash(fname)})
        return render_template("authentification.html", lname=lname, fname=fname)

#Authentification
@app.route('/mypage', methods=["GET", "POST"])
def auth1 ():

    if request.method == "GET":
        return render_template("form.html")
    else:
        username = request.form.get("fname")
        password = request.form.get("lname")
        user = mongo.db.user.find_one({'username':username})
        if user and check_password_hash(user['password'], password) :
            return render_template('mypage.html', username= username, passaword=password)
        else:
            flash('Username or password is not correct')


if __name__ == "__main__":
    app.run(host='localhost', port=5001, debug=True)