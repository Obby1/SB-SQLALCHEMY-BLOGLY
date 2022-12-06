from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Blogly."""
class User(db.Model):
    """User"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(50), nullable = False, unique= False)
    last_name = db.Column(db.String(50), nullable = False, unique= False)
    # image_url = db.Column(db.String(300), nullable = False, unique= False default = "https://i.stack.imgur.com/34AD2.jpg")
    image_url = db.Column(db.String(300), nullable = True, unique= False)




