from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser


class UserAdmin(admin.ModelAdmin):
    """
    Административная панель для управления объектами модели User.
    """

    UserAdmin.fieldsets += (
        ('Extra Fields', {'fields': ('is_admin',)}),
    )
    list_filter = ('email', 'username',)


admin.site.register(MyUser, UserAdmin)
