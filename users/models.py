from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)




class User(AbstractBaseUser):
    email= models.EmailField(verbose_name='email', max_length=60, unique=True)
    first_name=models.CharField(max_length=60, blank=True, null=True)
    last_name=models.CharField(max_length=60, blank=True, null=True)
    date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login= models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin= models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)

    objects=CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label ):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)