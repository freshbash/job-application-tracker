from django.http import JsonResponse
from django.db.models import Q
from application_tracker.models import Application

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
