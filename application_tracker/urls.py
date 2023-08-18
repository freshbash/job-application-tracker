from django.urls import path
from application_tracker.views import user_auth, render_templates, api

urlpatterns = [
    #User Auth
    path("registration", user_auth.registration_page, name="registration_page"),
    path("login_page", user_auth.login_page, name="login_page"),
    path("login", user_auth.login_user, name="login"),
    path("register", user_auth.register, name="register"),
    path("logout", user_auth.logout_user, name="logout"),

    #Render Templates
    path("", render_templates.index, name="index"),
    path("create", render_templates.create_application, name="create_application"),
    path("analytics", render_templates.view_analytics, name="view_analytics"),
    path("recruiters", render_templates.view_recruiters, name="view_recruiters"),
    path("companies", render_templates.view_companies, name="view_companies"),
    path("add_recruiter", render_templates.add_recruiter, name="add_recruiter"),
    path("profile", render_templates.view_profile, name="view_profile"),
    path("delete", render_templates.delete_account, name="delete_account"),

    #API
    path("api/applications/<str:type>", api.get_applications, name="get_applications"),
    path("api/get_recruiters", api.get_recruiters, name="get_recruiters"),
    path("api/get_companies", api.get_companies, name="get_companies"),
    path("api/delete_company/<int:c_id>", api.delete_company, name="delete_company"),
    path("api/delete_recruiter/<int:r_id>", api.delete_recruiter, name="delete_recruiter"),
    path("api/analytics", api.get_data, name="get_analytics_data"),
    path("api/modify_appl/<int:app_id>", api.modify_application, name="modify_application"),
    path("api/delete_appl/<int:app_id>", api.delete_application, name="delete_application"),
    path("api/get_links", api.get_links, name="get_links"),
    path("api/add_link", api.add_link, name="add_link"),
    path("api/modify_link", api.modify_link, name="modify_link"),
    path("api/delete_link", api.delete_link, name="delete_link")
]
