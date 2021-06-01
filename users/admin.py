from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *


admin.site.register(UserProfile)
# admin.site.unregister(Group)  # remove Group objects from admin page:  under[Authentication and Authorization]
