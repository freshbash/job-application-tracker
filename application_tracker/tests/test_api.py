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

    def test_get_applications(self):
        
        #Log the test_user in
        self.client.force_login(self.test_user)

        #Check whether non-GET requests are forbidden
        error_response = self.client.post(reverse("get_applications", args=["opn"]))

        #Check that the status code is 403
        self.assertEqual(error_response.status_code, 403)

        #Send a GET request to get_applications to get open applications
        opn_response = self.client.get(reverse("get_applications", args=["opn"]))

        #Check response is 302 found
        self.assertEqual(opn_response.status_code, 302)

        #Check that a valid json has been received or not
        opn_data = opn_response.json()

        self.assertEqual(opn_data[0]["role"], "Software Engineer")
        self.assertEqual(opn_data[0]["company"], "Google")
        self.assertEqual(opn_data[0]["description"], "Test Description")
        self.assertEqual(opn_data[0]["location"], "Munich, Germany")

        #Send a GET request to get_applications to get closed applications
        cls_response = self.client.get(reverse("get_applications", args=["cls"]))

        #Check response is 302 found
        self.assertEqual(cls_response.status_code, 302)

        #Check that a valid json has been received or not
        cls_data = cls_response.json()

        self.assertEqual(cls_data[0]["role"], "Software Engineer")
        self.assertEqual(cls_data[0]["company"], "Facebook")
        self.assertEqual(cls_data[0]["description"], "Test Description")
        self.assertEqual(cls_data[0]["location"], "Munich, Germany")


    #Test get_data
    def test_get_data(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Make a get request to get_analytics_data
        response = self.client.get(reverse("get_analytics_data"))

        #Check that the response is 302 found
        self.assertEqual(response.status_code, 302)

        #Check that a valid json has been received or not
        data = response.json()

        self.assertEqual(len(data), 2)
