from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UsersManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Учетная запись должна иметь адрес электронной почты.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    userid = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100) 
    description = models.CharField(max_length=500, blank=True, default='')
    startups = models.JSONField(default=list)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UsersManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.userid)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Startups(models.Model):
    owners = models.JSONField(default=list)
    startupid = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(unique=True, max_length=200)
    description = models.CharField(max_length=2000, blank=True, default='')
    picture = models.CharField(max_length=500, blank=True, default='')
    responses = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Стартап'
        verbose_name_plural = 'Стартапы'