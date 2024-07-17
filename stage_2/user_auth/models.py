from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, userId, firstName, lastName, email, password=None, phone=None):
        if not email:
            raise ValueError('User must have a valid email address')
        if not userId:
            raise ValueError("User must have a user Id")

        email = self.normalize_email(email)
        user = self.model(userId=userId, firstName=firstName, lastName=lastName, email=email, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, userId, firstName, lastName, email, password=None, phone=None ):
        user = self.create_user(userId, firstName, lastName, email, password, phone)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    userId = models.CharField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_id', 'firstName', 'lastName']

    def __str__(self):
        return self.email
