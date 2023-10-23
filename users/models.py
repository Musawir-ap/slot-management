from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin


# Create your models here.
class Role(models.Model):
    USER_TYPES = (
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
        ('STAFF', 'Staff'),
    )

    name = models.CharField(max_length=20, choices=USER_TYPES, unique=True, primary_key=True, editable=False)
    sub_roles = models.ManyToManyField('SubRole', default=None, editable=False)

    def __str__(self):
        name = self.name
        if name is None:
            print("Role __str__ method: name is None")
        return name
    

class SubRole(models.Model):
    name = models.CharField(max_length=20, unique=True, primary_key=True)
    main_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='subroles', null=True, editable=True)
    
    def __str__(self):
        name = self.name
        if name is None:
            print("subRole __str__ method: name is None")
        return name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.main_role:
            # Automatically set the filtered subroles for the role
            filtered_subroles = SubRole.objects.filter(main_role=self.main_role)
            self.main_role.sub_roles.set(filtered_subroles)
    
    
class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        try:
            admin_role = Role.objects.get(name='ADMIN')
        except Role.DoesNotExist:
            raise Exception("The 'ADMIN' role does not exist.")
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", admin_role)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("role") != admin_role:
            raise ValueError("Superuser must have role 'ADMIN'.")

        return self._create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE) 
    sub_roles = models.ManyToManyField(SubRole)
    
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password']
    objects = CustomUserManager()

    
    def __str__(self):
        return self.username
    
    # class Meta(AbstractUser.Meta):
    #     swappable = "AUTH_USER_MODEL"