from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.SUPER_ADMIN)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    SUPER_ADMIN = 'superadmin'
    
    ROLE_CHOICES = [
        (USER, 'User'),
        (ADMIN, 'Admin'),
        (SUPER_ADMIN, 'Super Admin'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)
    admin = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    objects = UserManager()
    
    def is_superadmin(self):
        return self.role == self.SUPER_ADMIN
    
    def is_admin(self):
        return self.role == self.ADMIN
    
    def is_regular_user(self):
        return self.role == self.USER
