from application_tracker.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse


#View to render the register page
def registration_page(request):
    if request.method == "GET":
        return render(request, "application_tracker/registration_page.html")

#View to render login page
def login_page(request):
    if request.method == "GET":
        return render (request, "application_tracker/login_page.html")

#View to handle user registration
def register(request):
    if request.method == "POST":
        #Get the new user's data
        username = request.POST["username"]
        password = request.POST["password"]
        website = request.POST["website"]
        github = request.POST["github"]
        linkedin = request.POST["linkedin"]

        #Create a new user
        new_user = User.objects.create_user(username=username, password=password, website_url=website, github_url=github, linkedin_url=linkedin)

        #Save the new user
        new_user.save()

        #Log the new user in
        login(request, new_user)

        #Redirect the user to the home page
        return HttpResponseRedirect(reverse("index"))
    
#View to handle user login
def login_user(request):
    if request.method == "POST":
        
        #Get login data
        username = request.POST["username"]
        password = request.POST["password"]

        #Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            #Log the user in
            login(request, user)

            #Redirect the user to the home page
            return HttpResponseRedirect(reverse("index"))
        else:
            #Redirect the user to the login page
            return render(request, "application_tracker/login_page.html", {"message": "Incorrect username/password"})
        
#View to handle user logout
def logout_user(request):
    logout(request)

    #Redirect the user to the landing page
    return HttpResponseRedirect(reverse("index"))
