from django.db import models


# Create your models here.
class router_details(models.Model):
    sapid = models.CharField(max_length=200, null=True, blank=True, unique=True)
    hostname = models.CharField(max_length=200, null=True, blank=True, unique=True)
    loopback = models.CharField(max_length=200, null=True, blank=True, unique=True)
    macaddress = models.CharField(max_length=200, null=True, blank=True, unique=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.hostname

    class Meta:
        db_table = 'router_details'
