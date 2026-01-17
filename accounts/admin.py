from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *

admin.site.register(MyUser, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(UserBlendInteraction)