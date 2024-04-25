from django.contrib import admin
from .models import Profile
from .models import Victory

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', "email") 

# admin.site.register(UserAdmin)
admin.site.register(Profile)
admin.site.register(Victory)