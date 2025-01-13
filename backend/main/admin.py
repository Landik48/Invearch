from django.contrib import admin
from .models import Users, Startups, StartupOwners, InterestedParties

class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'username')

admin.site.register(Users, UsersAdmin)
admin.site.register(Startups)
admin.site.register(StartupOwners)
admin.site.register(InterestedParties)