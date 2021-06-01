from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'created_at', 'updated_at', 'manager', 'shared_url',)
    list_editable = ('manager',)
    list_display_links = ('id', 'full_name',)
    list_per_page = 50
    search_fields = ('full_name', 'manager__username',)
    list_filter = ('created_at', 'manager', 'updated_at',)


class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_full_name', 'platform', 'deleted_names', 'added_project_names', 'action', 'manager', 'day',)
    list_editable = ('platform', 'action',)
    list_display_links = ('id', 'get_full_name',)
    list_per_page = 50
    search_fields = ('get_full_name', 'manager',)
    list_filter = ('platform', 'manager',)

    def get_full_name(self, instance):
        if instance.contact:
            return instance.contact.full_name
        else:
            return 'NA'

    get_full_name.short_description = 'Full Name'  # Renames column head

    def get_manager(self, instance):
        if instance.contact:
            return instance.contact.manager.username
        else:
            return 'NA'

    get_manager.short_description = 'Manager'  # Renames column head


admin.site.register(Laboratory)
admin.site.register(LabTechnician)
admin.site.register(Doctor)
admin.site.register(Sample)
admin.site.register(Test)
admin.site.register(Report)
# admin.site.register(Activity, ActivityAdmin)
admin.site.unregister(Group)  # remove Group objects from admin page:  under[Authentication and Authorization]
