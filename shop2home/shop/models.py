# myapp/models.py
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    items = models.CharField(max_length=1000)
    lat_long = models.CharField(max_length=100)
    full_details = models.TextField()

    def __str__(self):
        return self.name
