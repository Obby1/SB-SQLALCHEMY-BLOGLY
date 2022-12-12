# """Seed file to make sample data for db"""
# # python seed.py

# from models import db, first_name, last_name, image_url
# from app import app

# #Create all tables
# db.drop_all()
# db.create_all()

# user1 = User(first_name= "Ob", last_name="del")
# user2 = User(first_name="Mal", last_name="del")

# blog1 = Post(title="good title", content="great content", user_id=1)
# blog2 = Post(title="good title", content="great content", user_id=1)
# blog3 = Post(title="good title", content="great content", user_id=1)

# cooltag = Tag(name="cool")
# lametag = Tag(name = "lame")

# posttag1 = PostTag(post_id=1, tag_id=1)
# posttag2 = PostTag(post_id=2, tag_id=1)
# posttag3 = PostTag(post_id=3, tag_id=2)

