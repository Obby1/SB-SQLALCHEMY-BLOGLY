from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


db = SQLAlchemy()

# def connect_db(app):
#     db.app = app
#     db.init_app(app)
#     app.app_context().push()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

"""Models for Blogly."""
class User(db.Model):
    """User"""
    __tablename__ = 'users'
    # DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"
    id = db.Column(db.Integer, primary_key = True)
    # note - currently user can submit null first_name and still works. can try adding None or somehow forcing data inputs here. 
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    image_url = db.Column(db.String(300), default = DEFAULT_IMAGE_URL, nullable = False)
    # posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    # posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    #backref from user to post_tag table? ammend table structure?

    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        u = self
        return f"<User id = {self.id} first name = {self.first_name} last name = {self.last_name} link = {self.image_url}>"
        # return f"<Pet id = {self.id}>"

class Post(db.Model):
    """Post Model"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable = True, unique = False)
    content = db.Column(db.Text, nullable = True, unique = False)
    created_at = db.Column(db.DateTime(timezone=True), nullable = True, server_default=func.now())
    # time_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    # user = db.relationship('User', backref = 'posts')
    
    #access tags from posts and posts from tags
    # below wont work since tags and posts having nothing connecting them
    # tags = db.relationship('Tag', backref = 'posts')


    # set up m2m relationship between posts and tags
    post_tags = db.relationship('PostTag', backref = 'posts')

    # set up through relationship between posts and tags
    # backref to posts to see if avoids error?
    tags = db.relationship(
        'Tag', secondary = "posts_tags", backref = "posts"
    )

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    def __refr__(self):
        return f"<Post title: {self.title}, Post content: {self.content}, Post created at {self.created_at}>"

class Tag(db.Model):
    """model for tags"""
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable = False, unique = True)

    # set  up m2m relationship between posttags and tags
    post_tags = db.relationship('PostTag', backref = 'tags')

    # should tags have a foreign key ref to posts? or vice versa?

    @classmethod
    def get_tags(cls):
        tags = Tag.query.all()
        list_tags = []
        for tag in tags:
            list_tags.append(tag.name)
        return list_tags

    # def get_tags(self):
    #     tags = Tag.query.all()
    #     for tag in tags:
    #         list_tags.append(tag.name)
    def __refr__(self):
        return f"<Tag id: {self.id}, Tag name: {self.name}>"


class PostTag (db.Model):
    """mapping posts to tags"""
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True, nullable = False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True, nullable = False)
    


    __table_args__ = (
    db.PrimaryKeyConstraint(
        post_id, tag_id,
        ),
    )
    
    def __refr__(self):
        return f"<Tag id: {self.post_id}, Tag name: {self.tag_id}>"


def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()
