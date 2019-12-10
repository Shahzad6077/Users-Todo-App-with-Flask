from flask import Flask,render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import random
import string
app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# INITIALIZE THE DATABASE
db = SQLAlchemy(app)


def randomStringwithDigitsAndSymbols(stringLength=10):
    """Generate a random string of letters, digits and special characters """
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))


# db.create_all()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role=db.Column(db.String(40),nullable=False)
    name=db.Column(db.String(40),unique=True,nullable=True)
    pasword=db.Column(db.String(40),unique=False,nullable=True)
    email=db.Column(db.String(40),unique=False,nullable=True)
    phone=db.Column(db.String(40),unique=False,nullable=True)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# db.create_all()


# @app.route("/")
# def index():
#     return "Index Page"

@app.route("/main")
def main():
    return render_template("index.html")

@app.route("/", methods=['POST','GET'])
def add():
    if request.method == 'POST':
        getName = request.form['name']
        getEmail = request.form['email']
        getRole = request.form['role']
        getPhone = request.form['phone']

        newUser = User()
        newUser.name = getName
        newUser.email = getEmail
        newUser.role = getRole
        newUser.phone = getPhone
        newUser.pasword = randomStringwithDigitsAndSymbols(5)
        try:
            db.session.add(newUser)
            db.session.commit()
            return redirect("/")
        except:
            return "Error"
    else:
        # users = User.query.order_by.all.
       return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
