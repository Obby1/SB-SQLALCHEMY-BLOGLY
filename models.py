from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()


"""Models for Blogly."""
class User(db.Model):
    """User"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable = False, unique= False)
    last_name = db.Column(db.String(50), nullable = False, unique= False)
    # image_url = db.Column(db.String(300), nullable = False, unique= False default = "https://i.stack.imgur.com/34AD2.jpg")
    image_url = db.Column(db.String(300), nullable = True, unique= False)
    # posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"
    def __repr__(self):
        u = self
        return f"<User id = {u.id} first name = {u.first_name} last name = {u.last_name} link = {u.image_url}>"
        # return f"<Pet id = {self.id}>"

class Post(db.Model):
    """Post Model"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.Text, nullable = True, unique = False)
    content = db.Column(db.Text, nullable = True, unique = False)
    created_at = db.Column(db.DateTime(timezone=True), nullable = True, server_default=func.now())
    # time_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref = 'posts')
    
    def __refr__(self):
        return f"<Post title: {self.title}, Post content: {self.content}, Post created at {self.created_at}>"



