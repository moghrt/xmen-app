from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Falta email")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_superuser(self, email, password):
        user=self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user

class User(AbstractBaseUser, PermissionsMixin):

    USER_TYPE = (
        ("ALUMNO", "Alumno"),
        ("PROFESOR", "Profesor"),
        ("ADMIN", "Admin"),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    caption = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    user_type = models.CharField(max_length=25, choices=USER_TYPE, default='ALUMNO')
    tags = models.CharField(max_length=255, null=True, blank=True, default='')

    objects = UserManager()

    # Cambio mi campo de usuario por el de email
    USERNAME_FIELD = 'email'