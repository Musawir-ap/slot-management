from django.contrib import admin
from .models import Service, Token, Status
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    fields = ('name', 'code')
    
    def response_change(self, request, obj):
        if obj.is_default:
            messages.warning(request, "Sorry, you can't change the 'Other' service.")
            return HttpResponseRedirect(reverse('admin:tokenappcusotm_service_changelist'))
        return super().response_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        if Service.objects.filter(pk=obj_id, is_default=True).exists():
            messages.warning(request, "Sorry, you can't delete the 'Other' service.")
            return HttpResponseRedirect(reverse('admin:tokenappcusotm_service_changelist'))
        return super().response_delete(request, obj_display, obj_id)
    
    def custom_delete_action(self, request, queryset):
        if queryset.filter(name='Other', code='OTH').exists():
            messages.warning(request, "Sorry, you can't delete the 'Other' service.")
            queryset.exclude(name='Other', code='OTH').delete()
            return
        else:
            queryset.exclude(name='Other', code='OTH').delete()
            self.message_user(request, "Deleted selected items")

    custom_delete_action.short_description = "Delete selected services"

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions
    
    actions = [custom_delete_action]
    
admin.site.register(Service, ServiceAdmin)


class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'token_date', 'token_time', 'service', 'status_id', 'user')
    # fields = ('token_date', 'token_time', 'service','status',)
    
admin.site.register(Token, TokenAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', )
    
admin.site.register(Status, StatusAdmin)