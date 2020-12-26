import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Request(models.Model):
    address = models.GenericIPAddressField()
    datetime = models.DateTimeField()

    def __str__(self):
        return "address: " + self.address + " datetime: " + str(self.datetime)

    # Cierto si la solicitud ya ha superado EXCLUSION_PERIOD
    def need_update(self):
        return self.datetime < timezone.now() - datetime.timedelta(seconds=settings.EXCLUSION_PERIOD)