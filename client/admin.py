from django.contrib import admin
from users.models import CustomUser, Role
from .models import ClientProfile


class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'user')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = CustomUser.objects.filter(role=Role.objects.get(pk='USER'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(ClientProfile, ClientProfileAdmin)
