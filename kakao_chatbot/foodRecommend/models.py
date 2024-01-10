from django.db import models

# Create your models here.

class Restaurant(models.Model):
    restaurant = models.TextField()
    url = models.URLField()
    img = models.URLField()
    