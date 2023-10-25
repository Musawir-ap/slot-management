from django.contrib import admin
from users.models import CustomUser, Role
from .models import StaffProfile


class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'user')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = CustomUser.objects.filter(role=Role.objects.get(pk='STAFF'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(StaffProfile, StaffProfileAdmin)