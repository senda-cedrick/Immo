from django.contrib import admin
from app_users.models import LogUser, Profile, User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','noms','email','profile','is_active')
    list_filter = ('is_active', 'profile')
    search_fields = ('noms', 'email', 'username')

class LogAdmin(admin.ModelAdmin):
    list_display = ('id','user','action','created_at')
    list_filter = ('action',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(LogUser, LogAdmin)
