from django.db import models

# Create your models here.
class Book:
    class Book(models.Model):
        title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.id:
            max_id = Book.objects.aggregate(models.Max('id'))['id__max']
            self.id = max_id + 1 if max_id else 1
        super(Book, self).save(*args, **kwargs)


    def __str__(self):
        return f"id={self.id} title= {self.title} author= {self.author} published in the year {self.publication_year}"

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth, password, **extra_fields):
        if not email:
            raise ValueError('Email Field Must be set')
        if not date_of_birth:
            raise ValueError('Date of Birth Field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, date_of_birth=date_of_birth)
        user.set_password(password)

        return user

    def create_superuser(self, username, email, date_of_birth, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not date_of_birth:
            raise ValueError('Date of Birth is Required')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be Superuse')

        return self.create_user(username, email, date_of_birth, password, **extra_fields)


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField()

    objects = CustomUserManager()


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ('can_view', 'Can View'),
            ('can_create', 'Can Create'),
            ('can_edit', 'Can Edit'),
            ('can_delete', 'Can Delete'),
        ]
