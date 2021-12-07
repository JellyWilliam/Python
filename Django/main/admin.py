from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from main.models import *

admin.site.site_header = "*****"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Добро пожаловать!"


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ManagingOrganization)
admin.site.register(Request)
admin.site.register(Worker)
admin.site.register(TarifPay)
admin.site.register(AddBuilding)
admin.site.register(AddSteamShop)
admin.site.register(TarifBuild)
admin.site.register(News)


@admin.register(AdressForTarif)
class AdressForTarifCol(admin.ModelAdmin):
    list_display = ("manage_org", "sity", "locality", "street", "house")
