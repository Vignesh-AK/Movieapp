from django.db import models
from django.contrib.auth.models import AbstractUser
# class DeveloperAdmin(AbstractUser):



class Movies(models.Model):
    name = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to="media", null=True)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
     movies = models.ManyToManyField(Movies)


