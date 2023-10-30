from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SubRole, Role
from django.forms import CheckboxSelectMultiple
from .forms import UserCreationAdimForm


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
        
    
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # add_form = UserCreationAdimForm
    
    list_display = ('username', 'email', 'first_name', 'role', 'is_active')
    # list_filter = ('role',)
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('role','first_name', 'last_name', 'email', 'sub_roles')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
            (
                None,
                {
                    'classes': ('wide',),
                    'fields': ('username', 'password1', 'password2', 'role'),
                },
            ),
        )
    

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj:
            form.base_fields['sub_roles'].queryset = SubRole.objects.filter(main_role=obj.role)
            form.base_fields['sub_roles'].widget = CheckboxSelectMultiple()
            form.base_fields['sub_roles'].required = False

        return form
    
    # formfield_overrides = {
    #     models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    # }
    

admin.site.register(SubRole, SubRoleAdmin)
admin.site.register(CustomUser, CustomUserAdmin)



