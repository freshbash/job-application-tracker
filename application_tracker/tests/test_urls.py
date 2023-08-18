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
    "create_application": render_templates.create_application,
    "view_analytics": render_templates.view_analytics,
    "view_recruiters": render_templates.view_recruiters,
    "view_companies": render_templates.view_companies,
    "add_recruiter": render_templates.add_recruiter,
    "view_profile": render_templates.view_profile,
    "delete_account": render_templates.delete_account,
    "get_applications": api.get_applications,
    "get_recruiters": api.get_recruiters,
    "get_companies": api.get_companies,
    "delete_company": api.delete_company,
    "delete_recruiter": api.delete_recruiter,
    "get_analytics_data": api.get_data,
    "modify_application": api.modify_application,
    "delete_application": api.delete_application,
    "get_links": api.get_links,
    "add_link": api.add_link,
    "modify_link": api.modify_link,
    "delete_link": api.delete_link
}

class TestURLs(TestCase):

    #Tests to check if each url path invokes the correct view

    def test_urls(self):

        for (name, func) in function_dictionary.items():
            url = reverse(name)
            self.assertEqual(resolve(url).func, func, msg="Incorrect view function for url: " + url)
