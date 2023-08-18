from django.test import TestCase
from django.core.files import File
from application_tracker import models
import json

class TestModels(TestCase):

    #Set up code
    def setUp(self):

        #Create a test user
        self.test_user = models.User.objects.create(
            username = "abc",
            password = 123,
            email = "a@b.com",
            website_url = "www.w.com",
            linkedin_url = "www.l.com",
            github_url = "www.g.com"
        )

        #Create a test company
        self.test_company = models.Company.objects.create(
            name = "com",
            website = "www.c.com"
        )

        #Create a test recruiter
        self.test_recruiter = models.Recruiter.objects.create(
            tracked_by = self.test_user,
            name = "rec",
            company = self.test_company,
            email = "a@r.com",
            linkedin = "www.recatl.com"
        )

        #Create a test resume
        self.test_resume = models.Resume.objects.create(
            owned_by = self.test_user,
            doc_name = "res.pdf",
            doc_file = "res.pdf"
        )

    #Test the methods in User model
    def test_user(self):

        #Get the serialized test_user data
        jsonData = self.test_user.serialize()

        #Create a dictionay with test_user's data
        user_data = {
            "website": "www.w.com",
            "linkedin": "www.l.com",
            "github": "www.g.com"
        }

        #Serialize it!
        user_data_json = json.dumps(user_data)

        self.assertEquals(jsonData, user_data_json)
