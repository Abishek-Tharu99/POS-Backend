from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=15, unique=True)
    pan_no = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name