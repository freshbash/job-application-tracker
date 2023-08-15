from django.http import JsonResponse
from django.db.models import Q
from application_tracker.models import Application, Recruiter, Company, Analytics
import json


#API endpoint to get applications
def get_applications(request, type):

    #Only handle GET requests
    if request.method == "GET":
        
        #Create a list to store applications
        applications = []

        #check the type of applications to return
        if type == "opn":
            applications = list(Application.objects.filter(Q(status="APP") | Q(status="INP"), created_by=request.user).values())
        elif type == "cls":
            applications = list(Application.objects.filter(Q(status="REJ") | Q(status="ACC"), created_by=request.user).values())            
        elif type == "all":
            applications = list(Application.objects.filter(created_by=request.user).values())

        #Send an appropriate json response to the frontend
        if len(applications) == 0:
            return JsonResponse({"error": "No applications found."}, status=404)
        return JsonResponse({"applications" : applications}, status=302)
    else:
        return JsonResponse({"error": "GET request required."}, status=403)
    
#API endpoint to get analytics
def get_data(request):

    #Get application date and status of all applications made by the user sorted by date in ascending order
    applications = list(Analytics.objects.only("date", "status").filter(tracked_by=request.user).order_by("date").values())

    #Send a json response to the frontend
    if len(applications) == 0:
        return JsonResponse({"error": "No applications found."}, status=404)
    return JsonResponse({"applications" : applications}, status=302)


#API endpoint to modify an application
def modify_application(request, app_id):

    if request.method == "PUT":

        #Get the data in request body
        modified_data = json.loads(request.body)

        #Get the application
        application = Application.objects.get(pk=app_id)

        #Check if application status is changed
        if application.status != modified_data["status"]:
            #Check if the new status is accepted or rejected
            if modified_data["status"] in ["accepted", "rejected"]:
                #Update analytics
                app_data = Analytics.objects.get(tracked_by=request.user, application=application)
                app_data.status = modified_data["status"]
                app_data.save()

        #Make the modifications
        application.role = modified_data["role"]
        application.company_name = modified_data["company_name"]
        application.company_website = modified_data["company_website"]
        application.description = modified_data["description"]
        application.posting = modified_data["posting"]
        application.status = modified_data["status"]
        application.location = modified_data["location"]
        application.type = modified_data["type"]
        application.recruiter_name = modified_data["recruiter_name"]
        application.recruiter_email = modified_data["recruiter_email"]
        application.recruiter_linkedin = modified_data["recruiter_linkedin"]

        #Save the changes
        application.save()

        #Send a json response to the frontend
        return JsonResponse(status=204)


#API endpoint to delete an application
def delete_application(request, app_id):
    
    #Handle delete requests
    if request.method == "DELETE":

        #Get the application
        application = Application.objects.get(pk=app_id)

        #Delete the resume file attached to the application
        application.file.delete()

        #Delete the application
        application.delete()

        #Send a json response to the frontend
        return JsonResponse(status=204)
    
#API endpoint to get recruiters
def get_recruiters(request):

    #Handle GET requests
    if request.method == "GET":

        #Get the page number, if exists
        page = int(request.GET.get("pg", 1))

        #Get the recruiters for the respective page
        recruiters = list(Recruiter.objects.filter(tracked_by=request.user).values()[page*10-10:page*10])

        #Send an appropriate json response to the frontend
        if len(recruiters) == 0:
            return JsonResponse({"error": "No recruiters found."}, status=404)
        return JsonResponse({"recruiters": recruiters}, status=302)


#API endpoint to get companies
def get_companies(request):

    #Handle GET requests
    if request.method == "GET":

        #Get the page number, if exists
        page = int(request.GET.get("pg", 1))
        
        #Get the companies for the respective page
        companies = list(Company.objects.filter(tracked_by=request.user).values()[page*10-10:page*10])

        #Send a json response
        if len(companies) == 0:
            return JsonResponse({"error": "No companies found."}, status=404)
        return JsonResponse({"companies": companies}, status=302)