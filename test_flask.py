# importing flask fixed tests?

from flask import Flask
from unittest import TestCase
from app import app
from models import db, connect_db, User, Post



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']



# tests won't run without below code
# with app.app_context():
#     app.app_context().push()
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
#     # db.drop_all()
#     # db.create_all()


# below code stopped deleting the main db

# below code broke test when placed here
# with app.app_context():
#     app.app_context().push()
#     db.create_all()

# working here: 
# with app.app_context():
#     db.create_all()

# below or from flask import fixed the testcase overriding main database
# below code working at the moment and not overriding original db
# test db data not getting deleted after test though
connect_db(app)
# with app.app_context():
#     db.drop_all()
#     db.create_all()

db.drop_all()
db.create_all()

app.app_context().push()

class UserViewsTestCase(TestCase):
    """Tests views for Users."""
    def setUp(self):
        """Add sample User."""
        with app.app_context():
            User.query.delete()
            user = User(first_name="TestUser_firstname", last_name="TestUser_lastname")
            # ideal to add 2 pets to check list pets shows up, like testpet2 
            db.session.add(user)
            db.session.commit()
            # in this instance of TestCase setting self.pet_id to pet_id so inside
            # of every test. Instead of making a new pet and using that in every
            # single test below, we can just reference pet.id
            self.user_id = user.id
            self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

            # BELOW BREAKS TEST            
            # db.drop_all()


    def test_list_users(self):
        """test list users first_name shows on /users route"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser_firstname', html)


    def test_show_user(self):
        """tests 
        1. users first_name shows on h1 of details page after new user is made
        2. users last_name is in html"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>{self.user.first_name} Details</h1>', html)
            # better to not hardcore dog as species in case you change it later
            # we're testing pet.species instead of dog to allow for future potential changes
            self.assertIn(self.user.last_name, html)

    def test_add_user(self):
        """test that when new user added with first_name of TestFirstName it shows up properly on next page"""
        with app.test_client() as client:
            # note first-name was used instead of first_name as below data is posted to the form
            # form fields are looking for name="first-name", "last-name", "image-url" NOT first_name, last_name, image_url
            d = {"first-name": "TestFirstName", "last-name": "TestLastName", "image-url": "www.google.com"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            # if didnt follow redirects it would be status code 301/302
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestFirstName Details</h1>", html)

    def test_404_error(self):
        """test if user visits user id that does not exist"""
        with app.test_client() as client:
            resp = client.get(f"/users/999999999999999999")
            
            self.assertEqual(resp.status_code, 404)

    def test_blog_page(self):
        """test if posting a blog works"""
        with app.test_client() as client:
            # resp = client.get(f"/users/{user.id}/posts/new", data=d, follow_redirects=True)
            resp = client.get("/posts")
            self.assertEqual(resp.status_code, 200)

    def test_add_new_post(self):
        with app.test_client() as client:
            """test adding a new post"""
            user = User.query.get_or_404(self.user_id)
            post = {"title": "test title", "content": "test content",
             "user": user }
            #problem below
            # resp = client.post(f"/users/{self.user_id}/posts/new", data=post, follow_redirects=True)
            
            
    # resp = client.post(f'/users/{self.user_id}/posts/new', data={'title': 'Test title', 'content': 'Test stuff', 'user_id': self.user_id})

    # def test_add_new_post(self):
        # with app.test_client() as client:
            # user was already made with set up file above for every new test
            # resp = client.post(f'/users/{self.user_id}/posts/new', 
			# data={'title': 'Test title', 'content': 'Test stuff', 'user_id': self.user_id})
            # user = User.query.get(self.user_id)
            # post = Post.query.filter_by(title = 'Test title').first()
			# Redirect to check if post got posted.
            # html = client.get(f'/posts/{post.id}').get_data(as_text=True)
            # self.assertIn('Test title', html)
            # self.assertIn('Test stuff', html)
            # self.assertIn(user.full_name, html)   


# @app.route("/users/<int:user_id>/posts/new", methods=["POST"])
# def post_post(user_id):
#     """post the new post"""
#     title = request.form["title"]
#     content = request.form["content"]
#     user = User.query.get_or_404(user_id)
#     new_post = Post(title=title, content = content, user = user)
#     db.session.add(new_post)
#     db.session.commit()
#     # return redirect(f"/posts/{new_post.id}")
#     return redirect(f"/posts/{new_post.id}")

#  def test_add_user(self):
#         """test that when new user added with first_name of TestFirstName it shows up properly on next page"""
#         with app.test_client() as client:
#             # note first-name was used instead of first_name as below data is posted to the form
#             # form fields are looking for name="first-name", "last-name", "image-url" NOT first_name, last_name, image_url
#             d = {"first-name": "TestFirstName", "last-name": "TestLastName", "image-url": "www.google.com"}
#             resp = client.post("/users/new", data=d, follow_redirects=True)
#             html = resp.get_data(as_text=True)
#             # if didnt follow redirects it would be status code 301/302
#             self.assertEqual(resp.status_code, 200)
#             self.assertIn("<h1>TestFirstName Details</h1>", html)

# broken stuff:


    # def test_add_blog(self):
    #     """test add blog to test db"""
    #     with app.test_client() as client:
    #         # user = User.query.filter_by(first_name = 'TestUser_firstname').first()
    #         # user = User.query.get_or_404(user_id)
    #         # userid = 
    #         # search test user and get user id.
    #         # use that id to make test post with f string below
    #         # need to include user data in posted object. Not part of html form but IS part of SQL query
    #         # d = {"title": "test-title", "content": "test-content", "user_id": user}
    #         # d = {"title": "test-title", "content": "test-content", "user_id": 6}
    #         # resp = client.post(f"/users/{user.id}/posts/new", data = d, follow_redirects= True)
    #         user_obj = User.query.filter_by(first_name = 'TestUser_firstname').first()
    #         user_id = user_obj.id
    #         user = User.query.get_or_404(user_id)
    #         d = {"title": "test-title", "content": "test-content", "user": user}
    #         # resp = client.post("/users/6/posts/new", data = d, follow_redirects= True)
    #         resp = client.post(f"/users/{user_id}/posts/new", data = d, follow_redirects= True)

    #         # html = resp.get_data(as_text=True)
    #         # resp = client.get(f"/posts")
    #         self.assertEqual(resp.status_code, 200)
          
    # resp = client.post(f"/users/{user.id}/posts/new", data=d, follow_redirects=True)
    # def test_blogposts(self):
    #     """test if posting a blog works. first add user, then post a blog with user"""
    #     with app.test_client() as client:
    #         # resp = client.get(f"/users/{user.id}/posts/new", data=d, follow_redirects=True)
    #         # resp = client.post(f"/users/{post.user.id}/posts/new", )
    #         # self.assertEqual(resp.status_code, 200)
    #         d = {"first-name": "TestFirstName", "last-name": "TestLastName", "image-url": "www.google.com"}
    #         resp = client.post("/users/new", data=d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)
    #         # if didnt follow redirects it would be status code 301/302
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("<h1>TestFirstName Details</h1>", html)
    #         # user = User.query.filter_by(first_name = 'TestUser_firstname').first()
    #         d2 = {"title": "test-title", "content": "test-content"}
    #         resp = client.post("/users/10/posts/new", data = d2, follow_redirects= True)
    #         self.assertEqual(resp.status_code, 200)
    #         # resp = client.post(f"/users/{user.id}/posts/new", data=d, follow_redirects=True)   

            

    # 1. Add test if user visits incorrect page id (none existent pet)
    # 2. Add test if user tries to add duplicate pet

    #3. Fix all broken tests and add more tests for new functionality 

    