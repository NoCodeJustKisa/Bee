from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from beehive.models import User
# Register your models here.
admin.site.register(User, UserAdmin)

#бля я ебу чоли какова хуя в админке не пояявлется мой юзер sooooqa