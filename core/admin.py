from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import ModelAdmin, register




from .models import *

class UserProfile_Admin(admin.ModelAdmin):
    search_fields = ["name", 'city']
    list_filter = ["city"]
    list_per_page = 3



class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(ModelAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Event)
admin.site.register(Evaluation)
admin.site.register(EventJoin)
admin.site.register(Message)
