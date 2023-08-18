from django.test import TestCase, Client
from application_tracker.models import User, Application, Company, Recruiter, Link
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
            password="qBCatkk&4@s48669"            
        )

        #Create a link for test_user
        self.test_link = Link.objects.create(
            owner = self.test_user,
            title="LinkedIn",
            url="https://www.linkedin.com/test"
        )

        #Create 2 application instances
        self.open_application = Application.objects.create(
            created_by=self.test_user,
            role="Software Engineer",
            company_name="Google",
            company_website="www.google.com",
            posting="www.linkedin.com",
            description="Test description",
            location="Munich, Germany"
        )

        self.closed_application = Application.objects.create(
            created_by=self.test_user,
            role="Software Engineer",
            company_name="Facebook",
            company_website="www.facebook.com",
            posting="www.linkedin.com",
            description="Test description",
            status="ACC",
            location="Munich, Germany"
        )

        #Create a company
        self.test_company = Company.objects.create(
            tracked_by=self.test_user,
            name="Microsoft",
            website="www.microsoft.com"
        )

        #Create a recruiter
        self.test_recruiter = Recruiter.objects.create(
            tracked_by=self.test_user,
            name="papia",
            company=self.test_company,
            email="papia@microsoft.com",
            linkedin="www.linkedin.com/papia"
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

        self.assertEqual(len(opn_data["applications"]), 1)

        #Send a GET request to get_applications to get closed applications
        cls_response = self.client.get(reverse("get_applications", args=["cls"]))

        #Check response is 302 found
        self.assertEqual(cls_response.status_code, 302)

        #Check that a valid json has been received or not
        cls_data = cls_response.json()

        self.assertEqual(len(cls_data["applications"]), 1)


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

        self.assertEqual(len(data["applications"]), 1)

    #Test modify_application
    def test_modify_application(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Make a PUT request to modify_application
        response = self.client.put(reverse("modify_application", args=[0]), json.dumps({
            "role": "Backend Engineer",
            "company_name": "Google",
            "company_website": "https://www.google.com",
            "description": "Test description",
            "posting": "https://www.careers.google.com",
            "status": "rejected",
            "location": "Munich, Germany",
            "type": "full-time-onsite",
            "recruiter_name": "Gary John",
            "recruiter_email": "longjohns@googlerecruiting.com",
            "recruiter_linkedin": "https://www.linkedin.com/in/garyjohn"
        }))

        #Check that the response is 204 no content
        self.assertEqual(response.status_code, 204)

    #Test delete_application
    def test_delete_application(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Make a DELETE request to delete_application
        response = self.client.delete(reverse("delete_applications", args=[1]))

        #Check that the response is 204 no content
        self.assertEqual(response.status_code, 204)

        #Check the application is deleted from the database
        self.assertEqual(Application.objects.all().count(), 1)

    #Test functionality that fetches recruiters
    def test_get_recruiters(self):
        
        #Log the test_user in
        self.client.force_login(self.test_user)

        #Make a GET request to get_recruiters
        response = self.client.get(reverse("get_recruiters"))

        #Check if the status is 302 found
        self.assertEqual(response.status_code, 302)

        #Check if a recruiter object is recieved as json
        data = response.json()

        self.assertEqual(len(data["recruiters"]), 1)

    
    #Test API endpoint that fetches companies
    def test_get_companies(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Make a GET request to get_companies
        response = self.client.get(reverse("get_companies"))

        #Check if the status is 302 found
        self.assertEqual(response.status_code, 302)

        #Check if a company object is received as json
        data = response.json()
        self.assertEqual(len(data["companies"]), 1)

    
    #Test API endpoint that deletes a recruiter
    def test_delete_recruiter(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Send a DELETE  request to delete_recruiter
        response = self.client.delete(reverse("delete_recruiter", args=[0]))

        #Check if the response status code is 204
        self.assertEqual(response.status_code, 204)

        #Check if the recruiter object is deleted from the model
        self.assertEqual(Recruiter.objects.all().count(), 0)

    
    #Test API endpoint that deletes a company
    def test_delete_company(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Send a DELETE request to delete_company to delete the company named Microsoft
        response = self.client.delete(reverse("delete_company", args=[2]))

        #Check if the response status code is 204
        self.assertEqual(response.status_code, 204)

        #Check if the Microsoft company object is deleted
        self.assertEqual(Company.objects.all().count(), 2)


    #Test API endpoint to get all the user links
    def test_get_links(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Send a GET request to get_links
        response = self.client.get(reverse("get_links"))

        #Check if the status is 200 OK
        self.assertEqual(response.status_code, 200)

        #Check if the link object is fetched
        data = response.json()
        self.assertEqual(len(data["links"]), 1)

        self.assertEqual(data["links"][0]["title"], "LinkedIn")

    #Test API endpoint that adds a link
    def test_add_link(self):

        #Log the test_user in
        self.client.force_login(self.test_user)

        #Send a POST request to add_link
        response = self.client.post(reverse("add_link"), json.dumps({
            "title": "website",
            "url": "https://www.test.com"
        }))

        #Check if the response status code is 201
        self.assertEqual(response.status_code, 201)

    #Test API endpoint that modifies a link
    def test_modify_link(self):

        #Log the user in
        self.client.force_login(self.test_user)

        #Send a PUT request to modify_link
        response = self.client.put(reverse("modify_link"), json.dumps({
            "id": self.test_link.id,
            "title": "LinkedIN",
            "url": "https://www.linkedin.com/test-user"
        }))

        #Check if the response code is 204
        self.assertEqual(response.status_code, 204)

    #Test API endpoint that deletes a link
    def test_delete_link(self):

        #Log the user in
        self.client.force_login(self.test_user)

        #Send a DELETE request to delete_link
        response = self.client.delete(reverse("delete_link"), json.dumps({
            "id": self.test_link.id
        }))

        #Check if the response status code is 204
        self.assertEqual(response.status_code, 204)