from django.http import JsonResponse
from django.db.models import Q
from application_tracker.models import Application
import json

#Convert a queryset to a dictionary
def queryset_to_dict(qset):

    #Variable to store index
    i = 0

    #Output dictinary
    output = dict()

    #Iterate over the set
    for r in qset:

        output[i] = r.serialize()
        i += 1

    #Return the dictionary
    return output


#API endpoint to get applications
def get_applications(request, type):

    #Only handle GET requests
    if request.method == "GET":
        
        #check the type of applications to return
        if type == "opn":
            open_applications = Application.objects.filter(Q(status="APP") | Q(status="INP"), created_by=request.user)
            return JsonResponse(queryset_to_dict(open_applications), status=302)
        elif type == "cls":
            closed_applications = Application.objects.filter(Q(status="REJ") | Q(status="ACC"), created_by=request.user)
            return JsonResponse(queryset_to_dict(closed_applications), status=302)
    else:
        return JsonResponse({"error": "GET request required."}, status=403)
    
#API endpoint to get analytics
def get_data(request):

    #Get application date and status of all applications made by the user sorted by date in ascending order
    applications = Application.objects.only("applied_on", "status").filter(created_by=request.user).order_by("applied_on")

    #Send a json response to the frontend
    return JsonResponse(queryset_to_dict(applications), status=302)


#API endpoint to modify an application
def modify_application(request, app_id):

    if request.method == "PUT":

        #Get the data in request body
        modified_data = json.loads(request.body)

        #Get the application
        application = Application.objects.get(pk=app_id)

        #Make the modifications
        application.role = modified_data["role"]
        application.company.name = modified_data["company_name"]
        application.company.website = modified_data["company_website"]
        application.description = modified_data["description"]
        application.posting = modified_data["posting"]
        application.status = modified_data["status"]
        application.location = modified_data["location"]
        application.type = modified_data["type"]
        application.recruiter.name = modified_data["recruiter_name"]
        application.recruiter.email = modified_data["recruiter_email"]
        application.recruiter.linkedin = modified_data["recruiter_linkedin"]

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

        #Delete the application
        application.delete()

        #Send a json response to the frontend
        return JsonResponse(status=204)
