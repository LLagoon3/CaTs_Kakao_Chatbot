from django.db import models

# Create your models here.

class Menu(models.Model):
    date = models.DateField()
    time = models.TextField() 
    menu = models.TextField()
    restaurant = models.TextField()
     