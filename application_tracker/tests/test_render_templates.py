from django.test import TestCase, Client
from django.urls import reverse
from application_tracker import models

class TestRenderTemplates(TestCase):

    #Set up code
    def setUp(self):

        #Define a client
        self.client = Client()

        #Define a test user
        self.test_user = models.User.objects.create(
            username="test_user",
            password="qBCatkk&4@s48669",
            website="https://www.test.com",
            github="https://www.github.com/test",
            linkedin="https://www.linkedin.com/test"
        )

    def test_index(self):

        #Make a GET request to index when user is not authenticated
        response_u = self.client.get(reverse("index"))

        #Check if the response is 200
        self.assertEqual(response_u.status_code, 200)

        #Check if the correct template is rendered
        self.assertTemplateUsed(response_u, "application_tracker/landing.html")

        #Make a GET request to index when user is authenticated
        self.client.force_login(self.test_user)
        response_a = self.client.get(reverse("index"))

        #Check if the response is 200
        self.assertEqual(response_a.status_code, 200)

        #Check if the correct template is rendered
        self.assertTemplateUsed(response_a, "application_tracker/index.html")

    #Test create application
    def test_create_application(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Make a POST request to create application
        response = self.client.post(reverse("create_application"), {
            "role": "SWE",
            "description": "Test description",
            "posting": "https://www.test.com",
            "location": "Test location",
            "status": "Applied",
            "employment_type": "FLT-ON",
            "add_new_company": "true",
            "company_name": "Test company",
            "company_website": "https://www.test.com",
            "add_new_recruiter": "true",
            "recruiter_name": "Test recruiter",
            "recruiter_email": "rec@test.com",
            "recruiter_linkedin": "https://www.linkedin.com/rec",
            "resume_name": "resume.pdf",
            "resume": ""
        })

        #Check if the response is 200 OK
        self.assertEqual(response.status_code, 200)

        #Check if an application instance was created
        self.assertEqual(models.Application.objects.all().count(), 1)

        #Check if a company instance was created
        self.assertEqual(models.Company.objects.all().count(), 1)

        #Check if a recruiter instance was created
        self.assertEqual(models.Recruiter.objects.all().count(), 1)

    
    #def view analytics
    def test_view_analytics(self):
        
        #Log test_user in
        self.client.force_login(self.test_user)

        #Make a GET request to view_analytics
        response = self.client.get(reverse("view_analytics"))

        #Check if the response is 200 OK
        self.assertEqual(response.status_code, 200)
        
        #Check if the correct template is rendered
        self.assertTemplateUsed(response, "application_tracker/view_analytics.html")


    #Test view recruiters
    def test_view_recruiters(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Make a GET request to view recruiters
        response = self.client.get(reverse("view_recruiters"))

        #Check if the response is 200 OK
        self.assertEqual(response.status_code, 200)

        #Check if the correct template is rendered
        self.assertTemplateUsed(response, "application_tracker/view_recruiters.html")

    
    #Test view companies
    def test_view_companies(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Make a GET request to view companies
        response = self.client.get(reverse("view_companies"))

        #Check if the response is 200 OK
        self.assertEqual(response.status_code, 200)

        #Check if the correct template is rendered
        self.assertTemplateUsed(response, "application_tracker/view_companies.html")

    #Test functionality for adding a recruiter
    def test_add_recruiter(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Make a POST request to add_recruiter
        response = self.client.post(reverse("add_recruiter"), {
            "name": "barbora",
            "email": "barbora@productboard.com",
            "linkedin": "www.linkedin.com/barbora",
            "company": "productboard",
            "website": "www.productboard.com"
        })

        #Check if the response code is 302 Found
        self.assertEqual(response.status_code, 302)

    #Test the profile page
    def test_view_profile(self):

        #Log the test user in
        self.client.force_login(self.test_user)

        #Send a GET request to view_profile
        response = self.client.get(reverse("view_profile"))

        #Check that the response code is 200 OK
        self.assertEqual(response.status_code, 200)

        #Check if the correct template is used
        self.assertTemplateUsed(response, "application_tracker/profile.html")

    #Test the delete account functionality
    def test_delete_account(self):

        #Log the user in
        self.client.force_login(self.test_user)

        #Send a DELETE request to delete_account
        response = self.client.delete(reverse("delete_account"))

        #Check if the response status is 204
        self.assertEqual(response.status_code, 204)

        #Check whether the user is deleted
        self.assertEqual(models.User.objects.all().count(), 0)

        #Check if the correct template is rendered
        self.assertTemplateUsed(response, "application_tracker/landing.html")
