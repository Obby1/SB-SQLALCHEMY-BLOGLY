# importing flask fixed tests?

from flask import Flask
from unittest import TestCase
from app import app
from models import db, connect_db, User



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']




# tests won't run without below code
# with app.app_context():
#     db.drop_all()
#     db.create_all()


# below code stopped deleting the main db
app.app_context().push()

# with app.app_context():
#     db.create_all()

# below or from flask import fixed the testcase overriding main database
connect_db(app)

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


    # 1. Add test if user visits incorrect page id (none existent pet)
    # 2. Add test if user tries to add duplicate pet

    