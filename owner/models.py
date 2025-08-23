from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return str(self.name) + str(self.last_name)
