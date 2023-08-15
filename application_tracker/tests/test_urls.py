from django.test import TestCase
from django.urls import resolve, reverse
from application_tracker.views import user_auth, render_templates, api

#Dictionary with name for url paths as keys and view function names as values.
function_dictionary = {
    "registration_page": user_auth.registration_page,
    "login_page": user_auth.login_page,
    "login": user_auth.login_user,
    "register": user_auth.register,
    "logout": user_auth.logout_user,
    "index": render_templates.index,
    "get_applications": api.get_applications,
    "create_application_page": render_templates.create_application_page,
    "create_application": render_templates.create_application,
    "view_documents": render_templates.view_documents,
    "view_analytics": render_templates.view_analytics,
    "get_analytics_data": api.get_data,
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
            self.assertEqual(resolve(url).func, func, msg="Incorrect view function for url: " + url)
