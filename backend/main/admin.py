from django.contrib import admin
from .models import Users, Startups

class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'username')

admin.site.register(Users, UsersAdmin)
admin.site.register(Startups)