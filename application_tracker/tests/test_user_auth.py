from django.test import TestCase, Client
from django.urls import reverse
from application_tracker.views import user_auth
from application_tracker.models import User

class TestUserAuth(TestCase):

    #Set up code
    def setUp(self):

        #Set up a test client
        self.client = Client()

    #Test registration page
    def test_registration_page(self):

        #Send a GET request to the registration page
        response = self.client.get(reverse("registration_page"))

        #Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    #Test login page
    def test_login_page(self):

        #Send a GET request to the login page
        response = self.client.get(reverse("login_page"))
        
        #Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    #Test user registration
    def test_user_registration(self):

        #Send a POST request to the registration page
        response = self.client.post(reverse("register"), {
            "username": "test_user",
            "password": "qBCatkk&4@s48669",
            "website": "https://www.test.com",
            "github": "https://www.github.com/test",
            "linkedin": "https://www.linkedin.com/test"
        })

        #Check that the response is 302 Found
        self.assertEqual(response.status_code, 302)
        #Check that the user was created
        self.assertEqual(User.objects.all().count(), 1)

    #Test user login
    def test_user_login(self):

        #Create a test user
        test_user = User.objects.create_user(
            username="test_user_1",
            password="qBCatkk4@s48669"
        )

        #Send a POST request to the login page
        response = self.client.post(reverse("login"), {
            "username": "test_user_1",
            "password": "qBCatkk4@s48669"
        })

        #Check that the response is 302 Found
        self.assertEqual(response.status_code, 302)        
