# from django.db.models.signals import pre_save, post_save
# from tokenapp.models import Token, StatusHistory
# from django.dispatch import receiver

# @receiver(pre_save, sender=Token)
# def token_pre_save(sender, instance, created,  **kwargs):
#     # Set the status_was attribute to the current status of the object.
#     if created:
#         instance.status_was = instance.status

# def token_status_changed(sender, instance, **kwargs):
#     # If the status has changed, add it to the status history.
#     if instance.pk and instance.status != instance.status_was:
#         StatusHistory.objects.create(tracked_object=instance, status=instance.status)

# pre_save.connect(token_pre_save, sender=Token)
# post_save.connect(token_status_changed, sender=Token)