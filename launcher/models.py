from django.db import models

# Create your models here.
class Request(models.Model):
    address = models.GenericIPAddressField()
    datetime = models.DateTimeField()

    def __str__(self):
        return "address: " + self.address + " datetime: " + self.datetime 