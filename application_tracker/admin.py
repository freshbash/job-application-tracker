from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from application_tracker import models

class CustomUserAdmin(UserAdmin):
    pass

#Register the models
admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.Application)
admin.site.register(models.Company)
admin.site.register(models.Recruiter)
admin.site.register(models.Resume)
