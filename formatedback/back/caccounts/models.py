from django.core.validators import validate_email
from django.db import models
import jwt
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from datetime import timezone, timedelta, datetime


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError('Either email or phone must be set')
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        is_superuser = extra_fields.pop('is_superuser', None)
        return self._create_user(phone, email, password, **extra_fields)

    def _create_user(self, phone, email=None, password=None, **extra_fields):
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email', blank=False, validators=[validate_email])
    name = models.CharField(max_length=60, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон', unique=True)
    photo = models.ImageField(upload_to='media/photos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.name

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for tasks such as handling email.
        Typically, it returns the user's first and last name.
        Since we do not store the user's real name, we return their username.
        """
        return self.name

    def get_short_name(self):
        """
        This method is required by Django for tasks such as handling email.
        Typically, this would be the user's name.
        Since we do not store the user's real name, we return their username.
        """
        return self.name

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'email': self.email,
            'exp': int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        return token

    def has_module_perms(self, app_label):
        """
        Have perms to `app_label`?
        """
        return True

    def has_perm(self, perm, obj=None):
        """
        have certain perms?
        """
        return True

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"


