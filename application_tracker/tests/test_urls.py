from django.test import TestCase
from django.urls import resolve, reverse
from application_tracker.views.api import login, register
from application_tracker.views.render_templates import index, create_application, view_documents, view_analytics
from application_tracker.views.user_auth import get_applications, get_documents, add_document, delete_document, modify_application, delete_application

function_dictionary = {
    "login": login,
    "register": register,
    "index": index,
    "get_applications": get_applications,
    "create_application": create_application,
    "view_documents": view_documents,
    "get_documents": get_documents,
    "view_analytics": view_analytics,
    "add_document": add_document,
    "delete_document": delete_document,
    "modify_application": modify_application,
    "delete_application": delete_application
}

class TestURLs(TestCase):

    #Tests to check if each url path invokes the correct view

    def test_urls(self):

        for (name, func) in function_dictionary.items():
            url = reverse(name)
            self.assertEquals(resolve(url).func, func)
