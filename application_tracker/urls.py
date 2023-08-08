from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("", views.index, name="index"),
    path("api/applications/<str:type>", views.get_applications, name="get_applications"),
    path("create", views.create_application, name="create_application"),
    path("view", views.view_documents, name="view_documents"),
    path("api/documents", views.get_documents, name="get_documents"),
    path("analytics", views.view_analytics, name="view_analytics"),
    path("api/add", views.add_document, name="add_document"),
    path("api/deletedoc", views.delete_document, name="delete_document"),
    path("api/modify_appl", views.modify_application, name="modify_application"),
    path("api/delete_appl", views.delete_application, name="delete_application")
]
