"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
app.app_context().push()

debug = DebugToolbarExtension(app)

connect_db(app)

# run one time then delete or what?
db.create_all()

@app.route("/")
def home_page():
    """shows list of all pets in db"""
    users= User.query.all()
    # return "Welcome"
    return render_template("home.html", users=users)

@app.route("/users")
def show_users():
    """shows list of all pets in db"""
    users= User.query.all()
    # return "Welcome"
    return render_template("users.html", users=users)

@app.route("/users/new")
def add_new_user():
    """shows list of all pets in db"""
    users= User.query.all()
    # return "Welcome"
    return render_template("adduser.html", users=users)

@app.route("/users/new", methods=["POST"])
def create_new_user():
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/users/{new_user.id}")

@app.route('/users/<int:user_id>')
def show_new_user(user_id):
    """show details about a single pet"""
    # instead of writing method to check if pet is None, use get or 404
    user = User.query.get_or_404(user_id)
    # pet = Pet.query.get(pet_id)
    return render_template("details.html", user=user)

@app.route("/", methods=["POST"])
def create_user():
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    # currently this has no error handling life if server is off 
    # or if user enters duplicate name (has to be unique)
    # ideally you except the error and handle it 
    # perhaps redirect back to form and flash error message (dup name etc)
    return redirect(f"/{new_user.id}")

@app.route('/<int:user_id>')
def show_user(user_id):
    """show details about a single pet"""
    # instead of writing method to check if pet is None, use get or 404
    user = User.query.get_or_404(user_id)
    # pet = Pet.query.get(pet_id)
    return render_template("details.html", user=user)
