from django.db import models
from django.utils import timezone
from users.models import CustomUser
from django.urls import reverse


class Purpose(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, null=True)
    is_default = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.name == 'Other':
            self.is_default = True
            self.code = 'OTH'
        if self.is_default:
            if Purpose.objects.filter(name='Other', code='OTH').exists():   
                return 
        super(Purpose, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_default and self.name == 'Other' and self.code == 'OTH':
            return
        super(Purpose, self).delete(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name


class Token(models.Model):
    token_date = models.DateField(default=timezone.now)
    token_time = models.TimeField(default=timezone.now)
    purpose = models.ForeignKey(Purpose, on_delete=models.SET_NULL, null=True, blank=True)
    _purpose = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True)
    is_booked = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    token_modified = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    
    def get_token(self):
        return f'token {self.pk} for {self.Purpose if self.Purpose else self._Purpose}'
    
    def __str__(self):
        return f'{self.pk}'
    
    def get_absolute_url(self):
        return reverse("token-detail", kwargs={"pk": self.pk})
    