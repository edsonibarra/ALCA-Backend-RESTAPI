from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    owner_id_house = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return str(self.name) + str(self.last_name)


class BaseOwner(models.Model):
    nombre = models.CharField(null=True, blank=True)
    apellido_paterno = models.CharField(null=True, blank=True)
    apellido_materno = models.CharField(null=True, blank=True)
    telefono = models.CharField(null=True, blank=True)
    o_id = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre
