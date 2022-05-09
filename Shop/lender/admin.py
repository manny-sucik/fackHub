from django.contrib import admin
from .models import Lender

#added for is_active
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
#

#added for is_active
def apply_activation(modeladmin, request, queryset):
    for User in queryset:
        User.is_active = 1
        User.save()
    apply_activation.short_description = 'Activate Selected Users'

class LenderAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

class UserAdminCustom(UserAdmin):
   list_display = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active')
   list_filter = ('is_staff', 'is_superuser', 'is_active')
   search_fields = ('username', )
   ordering = ['-is_superuser', '-is_staff', '-is_active', 'username']

   actions = [apply_activation, ]
#end

#also added <, LenderAdmin> below
admin.site.register(Lender, LenderAdmin)


#added
admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)
#