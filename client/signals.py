from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from .models import ClientProfile
from staff.models import StaffProfile

@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role.name == "USER":
            if not hasattr(instance, 'clientprofile'):
                ClientProfile.objects.create(user=instance)
    else:
        if instance.role.name == "STAFF":
            try:
                client_profile = ClientProfile.objects.get(user=instance)
                client_profile.delete()
            except ClientProfile.DoesNotExist:
                pass
            
            
@receiver(post_save, sender=CustomUser)
def save_client_profile(sender, instance, **kwargs):
    if instance.role.name == "USER":
        instance.baseprofile.clientprofile.save()