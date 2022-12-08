"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post

app = Flask(__name__)


# app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False

debug = DebugToolbarExtension(app)

connect_db(app)


with app.app_context():
    db.create_all()
    # app.app_context().push()


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
    return render_template("users.html", users=users)

@app.route("/users/new")
def add_new_user():
    """shows list of all users in db"""
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
    """show details about a single user"""
    # instead of writing method to check if pet is None, use get or 404
    user = User.query.get_or_404(user_id)
    img = user.image_url
    # user = User.query.get(user_id)
    # pet = Pet.query.get(pet_id)
    return render_template("details.html", user=user, img=img)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """edit user details"""
    # instead of writing method to check if pet is None, use get or 404
    user = User.query.get_or_404(user_id)
    # pet = Pet.query.get(pet_id)
    return render_template("edituser.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def show_edited_user(user_id):
    edituser= User.query.get_or_404(user_id)
    edituser.first_name = request.form["first-name"]
    edituser.last_name = request.form["last-name"]
    edituser.image_url = request.form["image-url"]
    db.session.add(edituser)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect(f"/users")


############# POST ROUTES #############

@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    """show new posts page"""
    user = User.query.get_or_404(user_id)
    return render_template("newpost.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def post_post(user_id):
    """post the new post"""
    title = request.form["title"]
    content = request.form["content"]
    user = User.query.get_or_404(user_id)
    new_post = Post(title=title, content = content, user = user)
    db.session.add(new_post)
    db.session.commit()
    # return redirect(f"/posts/{new_post.id}")
    return redirect(f"/posts/{new_post.id}")

@app.route("/posts")
def show_posts():
    """shows list of all posts in db"""
    posts= Post.query.all()
    return render_template("posts.html", posts = posts)

@app.route('/posts/<int:post_id>')
def show_new_post(post_id):
    """show details about new post"""
    post = Post.query.get_or_404(post_id)
    return render_template("postdetails.html", post = post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """edit post details"""
    post = Post.query.get_or_404(post_id)
    return render_template("editpost.html", post = post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"] )
def show_editted_post(post_id):
    """show editted post"""
    editpost = Post.query.get_or_404(post_id)
    editpost.title = request.form["title"]
    editpost.content = request.form["content"]
    # editpost.user? I'm not updating the user, shouldnt have to call it
    db.session.add(editpost)
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f"/posts")


# @app.route("/users/<int:user_id>/edit", methods=["POST"])
# def show_edited_user(user_id):
#     edituser= User.query.get_or_404(user_id)
#     edituser.first_name = request.form["first-name"]
#     edituser.last_name = request.form["last-name"]
#     edituser.image_url = request.form["image-url"]
#     db.session.add(edituser)
#     db.session.commit()
#     return redirect(f"/users/{user_id}")



# TO DO:
    #1. write tests for error handling for error or 404 
    #2. flash message if error?
    #3. tests overwriting data
    #4. add query or get to all other get requests
