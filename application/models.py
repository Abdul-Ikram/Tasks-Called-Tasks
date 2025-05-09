from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

# class User(models.Model):
class DefaultUser(BaseUserManager):
    def create_user(self, email, user_name, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
#     username = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#     deleted_by = models.DateTimeField(null=True, blank=True)


class User(AbstractBaseUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'

class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'labels'


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    status = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tasks'
