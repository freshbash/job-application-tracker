from django.db import models
from django.contrib.auth.models import AbstractUser
import json

#User model to store all user data
class User(AbstractUser):

    website_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)

    #Return the details above in a JSON format
    def serialize(self):
        return json.dumps({
            "website": self.website_url,
            "linkedin": self.linkedin_url,
            "github": self.github_url
        })

    #Returns a string summary of an instance
    def __str__(self) -> str:
        return f"user: {self.username}"
    
#Model to store data for each job application
class Application(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="app_creator")
    role = models.CharField(max_length=64)
    company = models.ForeignKey("Company")
    applied_on = models.DateField(auto_now_add=True)
    description = models.TextField()
    posting = models.URLField()

    application_status_choices = [
        ("APP", "applied"), #Applicant made an application with the company
        ("INP", "interviews-ongoing"), #Interviews are ongoing between the company and the applicant
        ("REJ", "rejected"), #Applicant was rejected by the company
        ("ACC", "accepted") #Company made a offer and the applicant has accepted and joined the company
    ]

    status = models.CharField(
        max_length=3,
        choices=application_status_choices,
        default=application_status_choices[0][0]
    )

    location = models.CharField(max_length=64)
    
    employment_types = [
        ("FLT-ON", "full-time-onsite"),
        ("FLT-RE", "full-time-remote"),
        ("FLT-HY", "full-time-hybrid"),
        ("PRT-ON", "part-time-onsite"),
        ("PRT-RE", "part-time-remote"),
        ("PRT-HY", "part-time-hybrid"),
        ("CON-ON", "contract-onsite"),
        ("CON-RE", "contract-remote"),
        ("CON-HY", "contract-hybrid"),
        ("INT-ON", "intership-onsite"),
        ("INT-RE", "intership-remote"),
        ("INT-HY", "intership-hybrid"),
    ]

    type = models.CharField(
        max_length=6,
        choices=employment_types,
        default=employment_types[0][0]
    )

    recruiter = models.ForeignKey("Recruiter", null=True, blank=True)
    resume = models.ForeignKey("Resume", null=True, blank=True)

    #Return application instance in a dictionary format
    def serialize(self):

        #The output dictionary
        output = {
            "id": self.id,
            "created_by": self.created_by,
            "role": self.role,
            "company": self.company,
            "description": self.description,
            "posting": self.posting,
            "applied_on": self.applied_on,
            "status": self.status,
            "location": self.location,
            "type": self.type,
            "recruiter": self.recruiter,
            "resume": self.resume
        }

        #Return the dictionary
        return output


#Model to store company data
class Company(models.Model):
    tracked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_company")
    name = models.CharField(max_length=64)
    website = models.URLField()


#Model to store recruiter data
class Recruiter(models.Model):
    tracked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_recruiter")
    name = models.CharField(max_length=64)
    company = models.ForeignKey(Company, blank=True)
    email = models.EmailField(blank=True, default="No Email")
    linkedin = models.URLField(blank=True, default="No LinkedIn")

    #Return a Recruiter instance in a dictionary format
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "company": self.company,
            "email": self.email,
            "linkedin": self.linkedin
        }


#Model to store resume data
class Resume(models.Model):
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_files")
    doc_name = models.CharField(max_length=64)
    file = models.FileField(upload_to='')

    #Method to return serialized resume data
    def serialize(self):
        return {
            "id": self.id,
            "doc_name": self.doc_name,
            "file_data": self.file_path
        }
