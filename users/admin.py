from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SubRole, Role
from django.forms import CheckboxSelectMultiple

class SubRoleInline(admin.TabularInline):
    model = SubRole
    extra = 0

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [SubRoleInline]
    
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Role, RoleAdmin)


class SubRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_role')
    list_filter = ('main_role',)
        
    def save_model(self, request, obj, form, change):

        data = form.cleaned_data
        for key, value in data.items():
            print(f'{key}: {value}')
            
        obj.save()
        
        
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound


# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'role')
#     list_filter = ('role',)
    
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Define your custom fields and configurations here
    list_display = ('username', 'email', 'first_name', 'role', 'is_staff')
    # list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'sub_roles')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# admin.site.register(CustomUser, CustomUserAdmin)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj:
            # If you are editing an existing object, modify the form
            form.base_fields['sub_roles'].queryset = SubRole.objects.filter(main_role=obj.role)
            form.base_fields['sub_roles'].widget = CheckboxSelectMultiple()
            form.base_fields['sub_roles'].required = False

        return form
    
    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     try:
    #         object = super().get_object(request, object_id)
    #     except ObjectDoesNotExist:
    #         return HttpResponseNotFound()

    #     return super().change_view(request, object_id, form_url, extra_context)

admin.site.register(SubRole, SubRoleAdmin)
admin.site.register(CustomUser, CustomUserAdmin)



