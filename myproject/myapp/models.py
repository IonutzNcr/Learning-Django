from django.db import models

class Profile(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField()

class Victory(models.Model):
    user = models.CharField(max_length=100, default='Anonymous')
    content = models.CharField(max_length=100)
    date = models.DateTimeField()