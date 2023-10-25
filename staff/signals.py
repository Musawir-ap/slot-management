from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from .models import StaffProfile
from client.models import ClientProfile

@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role.name == "STAFF" or instance.role.name == "ADMIN":
            if not hasattr(instance, 'staffprofile'):
                StaffProfile.objects.create(user=instance)
    else:
        if instance.role.name == "USER":
            try:
                staff_profile = StaffProfile.objects.get(user=instance)
                staff_profile.delete()
            except StaffProfile.DoesNotExist:
                pass
            
            
# @receiver(post_save, sender=CustomUser)
# def save_client_profile(sender, instance, **kwargs):
#     if instance.role.name == "USER":
#         instance.clientprofile.save()

@receiver(post_save, sender=CustomUser)
def save_staff_profile(sender, instance, **kwargs):
    if instance.role.name == "STAFF" or instance.role.name == "ADMIN":
        instance.baseprofile.staffprofile.save()
