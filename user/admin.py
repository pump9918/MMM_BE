# from django.contrib import admin
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# # User 모델을 등록
# admin.site.register(User, BaseUserAdmin)
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, EditorProfile, Address

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False     
    verbose_name_plural = "profile"
    
class EditorProfileInline(admin.StackedInline):
    model = EditorProfile
    can_delete = False
    verbose_name_plural = "editor_profile"
    
class UserAdmin(BaseUserAdmin):  
    inlines = (ProfileInline, EditorProfileInline, )

# User 모델을 등록
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(EditorProfile)
admin.site.register(Address)