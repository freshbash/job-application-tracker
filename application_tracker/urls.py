from django.urls import path
from application_tracker.views import user_auth, render_templates, api

urlpatterns = [
    path("login", user_auth.login, name="login"),
    path("register", user_auth.register, name="register"),
    path("", render_templates.index, name="index"),
    path("api/applications/<str:type>", api.get_applications, name="get_applications"),
    path("create", render_templates.create_application, name="create_application"),
    path("view", render_templates.view_documents, name="view_documents"),
    path("api/documents", api.get_documents, name="get_documents"),
    path("analytics", render_templates.view_analytics, name="view_analytics"),
    path("api/analytics", api.get_analytics_data, name="get_analytics_data"),
    path("add", render_templates.add_document, name="add_document"),
    path("api/deletedoc", api.delete_document, name="delete_document"),
    path("api/modify_appl", api.modify_application, name="modify_application"),
    path("api/delete_appl", api.delete_application, name="delete_application")
]
