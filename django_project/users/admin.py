from django.contrib import admin
from users.forms import UserRegisterForm, UserRegisterFormByAdmin
from users.models import extendedUser

class YourModelAdmin(admin.ModelAdmin):
    form = UserRegisterFormByAdmin

admin.site.register(extendedUser, YourModelAdmin)