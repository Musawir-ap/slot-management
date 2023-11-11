from typing import Any
from django.db import models
from django.utils import timezone
from users.models import CustomUser
from django.urls import reverse


class Service(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    code = models.CharField(max_length=10, null=True)
    is_default = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.name == 'Other':
            self.is_default = True
            self.code = 'OTH'
        if self.is_default:
            if Service.objects.filter(name='Other', code='OTH').exists():   
                return 
        super(Service, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_default and self.name == 'Other' and self.code == 'OTH':
            return
        super(Service, self).delete(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=20, unique=True, primary_key=True)
    description = models.TextField(null=True, blank=True)
    
    
class StatusHistory(models.Model):
    tracked_object = models.ForeignKey('Token', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)


class Token(models.Model):
    token_date = models.DateField(default=timezone.now)
    token_time = models.TimeField(default=timezone.now)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='tokens_for_service')
    custom_service = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True)
    is_booked = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='tokens_created_by_user')
    token_modified = models.DateTimeField(auto_now_add=True)
    assigned_staff = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='tokens_assigned_to_staff')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='tokens_with_status' ,default='Pending')
    status_was = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='tokens_with_status_was', null=True, blank=True)
    status_history = models.ManyToManyField(Status, through='StatusHistory', related_name='tokens_in_status_history')

            
    def get_token(self):
        return f'token {self.pk} for {self.Service if self.Service else self._Service}'
    
    def __str__(self):
        return f'{self.pk}'
    
    def get_absolute_url(self):
        return reverse("token-detail", kwargs={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        if self.pk:
            if self.status_was.pk != self.status.pk:
                StatusHistory.objects.create(tracked_object=self, status=self.status)
            self.status_was = Token.objects.get(pk=self.pk).status
            
        if not self.pk:
            super(Token, self).save(*args, **kwargs)
            self.status_was = self.status
            if self.status_was != self.status.pk:
                StatusHistory.objects.create(tracked_object=self, status=self.status)
            
        super(Token, self).save(*args, **kwargs)
        # # if 
        # StatusHistory.objects.create(tracked_object=self, status=self.status)
        