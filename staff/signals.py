from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from .models import StaffProfile
from client.models import ClientProfile
from django.db import transaction


# @receiver(post_save, sender=CustomUser)
# def create_or_update_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.role.name == "STAFF" or instance.role.name == "ADMIN":
#             with transaction.atomic():
#                 if not hasattr(instance, 'staffprofile'):
#                     StaffProfile.objects.create(user=instance)
#     else:
#         if instance.role.name == "USER":
#             try:
#                 staff_profile = StaffProfile.objects.get(user=instance)
#                 staff_profile.delete()
#             except StaffProfile.DoesNotExist:
#                 pass
            

@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role.name == "STAFF" or instance.role.name == "ADMIN":
            with transaction.atomic():
                try:
                    existing_profile = StaffProfile.objects.get(user=instance)
                    # logger.error(f"Conflicting staff_id detected for user {instance.username}")
                    pass
                except StaffProfile.DoesNotExist:
                    StaffProfile.objects.create(user=instance)

    else:
        if instance.role.name == "USER":
            try:
                staff_profile = StaffProfile.objects.get(user=instance)
                staff_profile.delete()
            except StaffProfile.DoesNotExist:
                pass

@receiver(post_save, sender=CustomUser)
def save_staff_profile(sender, instance, **kwargs):
    if instance.role.name == "STAFF" or instance.role.name == "ADMIN":
        try:
            staff_profile = instance.baseprofile.staffprofile
            staff_profile.save()
        except StaffProfile.DoesNotExist:
            # Handle the case where the profile doesn't exist (log or create it)
            pass
        
        
# @receiver(post_save, sender=CustomUser)
# def save_client_profile(sender, instance, **kwargs):
#     if instance.role.name == "USER":
#         instance.clientprofile.save()

# @receiver(post_save, sender=CustomUser)
# def save_staff_profile(sender, instance, **kwargs):
#     if instance.role.name == "STAFF" or instance.role.name == "ADMIN":
#         instance.baseprofile.staffprofile.save()