from django.db import models
from users.models import BaseProfile
import uuid


class StaffProfile(BaseProfile):
    staff_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=25)
    qualifications = models.TextField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username}\'s Profile'