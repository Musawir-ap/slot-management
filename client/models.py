from django.db import models
from users.models import BaseProfile
import uuid


class ClientProfile(BaseProfile):
    client_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mobile_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}\'s Profile'