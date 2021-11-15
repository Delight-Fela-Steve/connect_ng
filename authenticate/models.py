from django.contrib.auth.models import AbstractUser, AbstractBaseUser
# from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class User(AbstractBaseUser):
    email= models.EmailField(verbose_name='email', max_length=60, unique=True)
    username= models.CharField(max_length=30,unique=True)
    date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login= models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin= models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label ):
        return True


# class CustomBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         # UserModel = get_user_model()
#         try:
#             # user = UserModel.objects.get(email=email)
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None