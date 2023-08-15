from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from application_tracker import models


#Render the index page
def index(request):

    #Check if the user is authenticated
    if request.user.is_authenticated:

        #Render the home page
        return render(request, "application_tracker/index.html", status=200)

    else:

        #Render landing page
        return render(request, "application_tracker/landing.html", status=200)
        

#Render the create application page
@login_required(redirect_field_name="create", login_url="login_page")
@transaction.atomic
def create_application(request):
        
    if request.method == "POST":

        #Get the data from the form
        role = request.POST["role"]
        description = request.POST["description"]
        posting = request.POST["posting"]
        location = request.POST["location"]
        status = request.POST["status"]
        employment_type = request.POST["employment_type"]

        #Check if the the already exists in the database
        add_new_company = True if request.POST["add_new_company"] == "true" else False

        company = None

        if add_new_company:
            co_name = request.POST["company_name"].toLowerCase()
            website = request.POST["company_website"]

            #Check if a company with the same name already exists
            try:
                company = models.Company.objects.get(name=co_name)
            except models.Company.DoesNotExist:
                company = models.Company.objects.create(tracked_by=request.user, name=co_name, website=website)
                company.save()
        else:

            #Get the company object from the database
            try:
                company = models.Company.objects.get(tracked_by=request.user, id=int(request.POST["company_id"]))
            except models.Company.DoesNotExist:
                pass
        
        #Check if user has added details for a new recruiter
        add_new_recruiter = True if request.POST["add_new_recruiter"] == "true" else False

        recruiter = None

        #If the user has added details for a new recruiter, create a new recruiter object
        if add_new_recruiter:
            rec_name = request.POST["recruiter_name"].toLowerCase()
            email = request.POST["recruiter_email"]
            linkedin = request.POST["recruiter_linkedin"]

            #Check if a recruiter with the same name already exists
            try:
                recruiter = models.Recruiter.objects.get(name=rec_name, company=company, email=email, linkedin=linkedin)
            except models.Recruiter.DoesNotExist:
                #Create a new recruiter object
                recruiter = models.Recruiter.objects.create(
                    tracked_by=request.user,
                    name=rec_name,
                    company=company,
                    email=email,
                    linkedin=linkedin
                )
                recruiter.save()
        else:
            #Get the recruiter object from the database
            try:
                recruiter = models.Recruiter.objects.get(tracked_by=request.user, id=int(request.POST["recruiter_id"]))
            except models.Recruiter.DoesNotExist:
                pass

        #Get the uploaded file
        pdf = request.FILES.get("resume")
        #Store the original file name
        file_name = pdf.name


        #Create a new application object
        new_application = models.Application(
            created_by=request.user,
            role=role,
            company_name=company.name,
            company_website=company.website,
            description=description,
            posting=posting,
            location=location,
            status=status,
            employment_type=employment_type,
            recruiter_name=recruiter.name,
            recruiter_email=recruiter.email,
            recruiter_linkedin=recruiter.linkedin,
            resume_name=file_name,
        )

        #Create a new file name for the resume
        pdf.name = f"{request.user.id}_{new_application.id}_{file_name}"

        #Attach the file to the application
        new_application.file = pdf

        #Save the new application object
        new_application.save()

        #Redirect to the home page
        return HttpResponseRedirect(reverse("index"))
    

#Render the analytics
@login_required(redirect_field_name="create", login_url="login_page")
def view_analytics(request):

    #Render the analytics page
    return render(request, "application_tracker/analytics.html")


#Render the recruiters page
@login_required(redirect_field_name="create", login_url="login_page")
def view_recruiters(request):
    
        #Render the recruiters page
        return render(request, "application_tracker/recruiters.html")


#Render the companies page
@login_required(redirect_field_name="create", login_url="login_page")
def view_companies(request):

    #Render the companies page
    return render(request, "application_tracker/companies.html")
