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

    #Test create application page
    def test_create_application_page(self):

        #Log the user in
        self.client.force_login(self.test_user)

        #Make a GET request to create application page
        response = self.client.get(reverse("create_application_page"))

        #Check if the response is 200 OK
        self.assertEqual(response.status_code, 200)

        #Check if the correct template is rendered
        self.assertTemplateUsed(response, "application_tracker/create_application.html")

    #Test create application
    def test_create_application(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Make a POST request to create application
        response = self.client.post(reverse("create_application"), {
            "role": "SWE",
            "description": "Test description",
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
            "add_new_resume": "false",
            "resume_id": ""
        })

        #Check if the response is 200 OK
        self.assertEqual(response.status_code, 200)

        #Check if an application instance was created
        self.assertEqual(models.Application.objects.all().count(), 1)

        #Check if a company instance was created
        self.assertEqual(models.Company.objects.all().count(), 1)

        #Check if a recruiter instance was created
        self.assertEqual(models.Recruiter.objects.all().count(), 1)

    
    #Test view documents
    def test_view_documents(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Make a GET request to view documents
        response = self.client.get(reverse("view_documents"))

        #Check if the correct template is rendered
        self.assertTemplateUsed(response, "application_tracker/view_documents.html")

        #Check if the context is passed
        self.assertNotEqual(response.context.get("documents", ""), "")

    #Test add document
    def test_add_document(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        response = None

        #Make a POST request to add document
        with open("hello.pdf", "rb") as f:
            response = self.client.post(reverse("add_document"), {
                "new_resume": f
            })

        #Check if the response is 201 Created
        self.assertEqual(response.status_code, 201)

        #Check if a resume instance was created
        self.assertEqual(models.Resume.objects.all().count(), 1)

    #Test delete document
    def test_delete_document(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Create a resume instance
        resume = models.Resume.objects.create(
            user=self.test_user,
            resume="hello.pdf"
        )

        #Make a POST request to delete document
        response = self.client.post(reverse("delete_document"), {
            "resume_id": resume.id
        })

        #Check if the response is 200 OK
        self.assertEqual(response.status_code, 200)

        #Check if the resume instance was deleted
        self.assertEqual(models.Resume.objects.all().count(), 0)

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
