from django.db import models
from picklefield.fields import PickledObjectField
from django.contrib.auth.models import AbstractBaseUser ,BaseUserManager

class CustomUserManager(BaseUserManager):
        def create_user(self, email, username, UserFile,profilePic):
            if not email:
                raise ValueError('Users must have an email address')
            if not username:
                raise ValueError('Users must have a username')

            user = self.model(
                email=self.normalize_email(email),
                username=username,
                UserFile=UserFile,
                profilePic=profilePic,
            )

            
            user.save(using=self._db)
            return user

        def create_superuser(self, email, username, password,UserFile=None,profilePic=None):
            user = self.create_user(
                email=self.normalize_email(email),
                username=username,
                UserFile=None,
                profilePic=None,
            )
            user.set_password(password)
            user.is_admin = True
            user.is_staff = True
            user.is_superuser = True
            user.save(using=self._db)
            return user
class CustomUser(AbstractBaseUser):
        username=models.CharField(max_length=30 , unique=True)
        UserFile = PickledObjectField(null=True)
        date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
        email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
        profilePic=models.ImageField(upload_to='uploads/')
        last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
        is_admin				= models.BooleanField(default=False)
        is_active				= models.BooleanField(default=True)
        is_staff				= models.BooleanField(default=False)
        is_superuser			= models.BooleanField(default=False)


        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = ['email']

        objects = CustomUserManager()

        def __str__(self):
            return self.username

        # For checking permissions. to keep it simple all admin have ALL permissons
        def has_perm(self, perm, obj=None):
            return self.is_admin

        # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
        def has_module_perms(self, app_label):
            return True