from django.urls import path
from application_tracker.views import user_auth, render_templates, api

urlpatterns = [
    #User Auth
    path("registration", user_auth.registration_page, name="registration_page"),
    path("login_page", user_auth.login_page, name="login_page"),
    path("login", user_auth.login, name="login"),
    path("register", user_auth.register, name="register"),
    path("logout", user_auth.logout, name="logout"),

    #Render Templates
    path("", render_templates.index, name="index"),
    path("new", render_templates.create_application_page, name="create_application_page"),
    path("create", render_templates.create_application, name="create_application"),
    path("view", render_templates.view_documents, name="view_documents"),
    path("add", render_templates.add_document, name="add_document"),
    path("deletedoc/<int:doc_id>", api.delete_document, name="delete_document"),
    path("analytics", render_templates.view_analytics, name="view_analytics"),

    #API
    path("api/applications/<str:type>", api.get_applications, name="get_applications"),
    path("api/analytics", api.get_data, name="get_analytics_data"),
    path("api/modify_appl/<int:app_id>", api.modify_application, name="modify_application"),
    path("api/delete_appl/<int:app_id>", api.delete_application, name="delete_application")
]
