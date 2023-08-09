from django.db import models
from django.contrib.auth.models import AbstractUser

#User model to store all user data
class User(AbstractUser):

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

    application_status_choices = [
        ("APP", "Applied"),
        ("INP", "Interviews ongoing"),
        ("REJ", "Rejected"),
        ("ACC", "Accepted")
    ]

    status = models.CharField(
        max_length=3,
        choices=application_status_choices,
        default=application_status_choices[0][0]
    )

    location = models.CharField(max_length=64)
    
    employment_types = [
        ("FLT-ON", "Full-time onsite"),
        ("FLT-RE", "Full-time remote"),
        ("FLT-HY", "Full-time hybrid"),
        ("PRT-ON", "Part-time onsite"),
        ("PRT-RE", "Part-time remote"),
        ("PRT-HY", "Part-time hybrid"),
        ("CON-ON", "Contract onsite"),
        ("CON-RE", "Contract remote"),
        ("CON-HY", "Contract hybrid"),
        ("INT-ON", "Intership onsite"),
        ("INT-RE", "Intership remote"),
        ("INT-HY", "Intership hybrid"),
    ]

    type = models.CharField(
        max_length=6,
        choices=employment_types,
        default=employment_types[0][0]
    )

    recruiter = models.ForeignKey("Recruiter", null=True, blank=True)
    resume = models.ForeignKey("Resume", null=True, blank=True)


#Model to store company data
class Company(models.Model):
    name = models.CharField(max_length=64),
    website = models.URLField()


#Model to store recruiter data
class Recruiter(models.Model):
    name = models.CharField(max_length=64),
    email = models.EmailField()
    linkedin = models.URLField()


#Model to store resume data
class Resume(models.Model):
    doc_name = models.CharField(max_length=64)
    file_path = models.FileField()
