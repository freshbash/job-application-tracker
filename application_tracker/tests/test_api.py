from django.test import TestCase, Client
from application_tracker.models import User, Application
from django.urls import reverse
import json

#Testing for all views in application_tracker/views/api.py
def TestAPI(TestCase):

    #Set up code
    def setUp(self):
        
        #Create a client
        self.client = Client()

        #Create a test user
        self.test_user = User.objects.create_user(
            username="test_user",
            password="qBCatkk&4@s48669",
            website="https://www.test.com",
            github="https://www.github.com/test",
            linkedin="https://www.linkedin.com/test"
        )

    def test_get_applications(self):
        
        #Log the test_user in
        self.client.force_login(self.test_user)

        #Check whether non-GET requests are forbidden
        error_response = self.client.post(reverse("get_applications", args=["opn"]))

        #Check that the status code is 403
        self.assertEqual(error_response.status_code, 403)

        #Create 2 application instances
        open_application = Application.objects.create(
            created_by=self.test_user,
            role="Software Engineer",
            company="Google",
            description="Test description",
            location="Munich, Germany"            
        )

        closed_application = Application.objects.create(
            created_by=self.test_user,
            role="Software Engineer",
            company="Facebook",
            description="Test description",
            status="ACC",
            location="Munich, Germany"
        )

        #Send a GET request to get_applications to get open applications
        opn_response = self.client.get(reverse("get_applications", args=["opn"]))

        #Check response is 302 found
        self.assertEqual(opn_response.status_code, 302)

        #Check that a valid json has been received or not
        opn_data = opn_response.json()

        self.assertEqual(opn_data["role"], "Software Engineer")
        self.assertEqual(opn_data["company"], "Google")
        self.assertEqual(opn_data["description"], "Test Description")
        self.assertEqual(opn_data["location"], "Munich, Germany")

        #Send a GET request to get_applications to get closed applications
        cls_response = self.client.get(reverse("get_applications", args=["cls"]))

        #Check response is 302 found
        self.assertEqual(cls_response.status_code, 302)

        #Check that a valid json has been received or not
        cls_data = cls_response.json()

        self.assertEqual(cls_data["role"], "Software Engineer")
        self.assertEqual(cls_data["company"], "Facebook")
        self.assertEqual(cls_data["description"], "Test Description")
        self.assertEqual(cls_data["location"], "Munich, Germany")        
