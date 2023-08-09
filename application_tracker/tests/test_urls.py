from django.test import TestCase
from django.urls import resolve, reverse
from application_tracker.views import user_auth, render_templates, api

#Dictionary with name for url paths as keys and view function names as values.
function_dictionary = {
    "login": user_auth.login,
    "register": user_auth.register,
    "index": render_templates.index,
    "get_applications": api.get_applications,
    "create_application": render_templates.create_application,
    "view_documents": render_templates.view_documents,
    "get_documents": api.get_documents,
    "view_analytics": render_templates.view_analytics,
    "get_analytics_data": api.get_analytics_data,
    "add_document": render_templates.add_document,
    "delete_document": api.delete_document,
    "modify_application": api.modify_application,
    "delete_application": api.delete_application
}

class TestURLs(TestCase):

    #Tests to check if each url path invokes the correct view

    def test_urls(self):

        for (name, func) in function_dictionary.items():
            url = reverse(name)
            self.assertEquals(resolve(url).func, func)
