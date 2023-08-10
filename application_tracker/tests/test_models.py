from django.test import TestCase
from django.core.files import File
from application_tracker import models
import json
import datetime

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

    
    #Test the methods in Application model
    def test_application(self):

        #Create a test application
        test_application = models.Application.objects.create(
            created_by = self.test_user,
            role = "role",
            company = self.test_company,
            description = "description",
            applied_on = "2020-01-01",
            status = "APP",
            location = "location",
            type = "FLT-ON",
            recruiter = self.test_recruiter,
            resume = self.test_resume
        )

        #Get the serialized test_application data
        serializedOutput = test_application.serialize()

        #Check the type of each field
        self.assertEqual(type(serializedOutput["id"]), int)
        self.assertEqual(type(serializedOutput["created_by"]), int)
        self.assertEqual(type(serializedOutput["role"]), str)
        self.assertEqual(type(serializedOutput["company"]), models.Company)
        self.assertEqual(type(serializedOutput["description"]), str)
        self.assertEqual(type(serializedOutput["applied_on"]), datetime.date)
        self.assertEqual(type(serializedOutput["status"]), str)
        self.assertEqual(type(serializedOutput["location"]), str)
        self.assertEqual(type(serializedOutput["type"]), str)
        self.assertEqual(type(serializedOutput["recruiter"]), models.Recruiter)
        self.assertEqual(type(serializedOutput["resume"]), models.Resume)


    #Test the methods in Company model
    def test_recruiter(self):
        
        #Get the serialized test_recruiter data
        serializedOutput = self.test_recruiter.serialize()

        #Check the type of each field
        self.assertEqual(type(serializedOutput["id"]), int)
        self.assertEqual(type(serializedOutput["name"]), str)
        self.assertEqual(type(serializedOutput["company"]), models.Company)
        self.assertEqual(type(serializedOutput["email"]), str)
        self.assertEqual(type(serializedOutput["linkedin"]), str)


    #Test the methods in Resume model
    def test_resume(self):

        #Get the serialized test_resume data
        serializedOutput = self.test_resume.serialize()

        #Check the type of each field
        self.assertEqual(type(serializedOutput["id"]), int)
        self.assertEqual(type(serializedOutput["doc_name"]), str)
        self.assertEqual(type(serializedOutput["file_data"]), File)
