# models.py
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import os
from owner.models import Owner


def property_image_upload_path(instance, filename):
    """Función para definir la ruta de subida de imágenes"""
    # Obtiene la extensión del archivo
    ext = filename.split('.')[-1]
    # Crea un nombre único basado en el modelo y ID
    model_name = instance.content_object._meta.model_name
    object_id = instance.object_id
    return f'properties/{model_name}/{object_id}/{filename}'


class PropertyImage(models.Model):
    """Modelo genérico para manejar imágenes de cualquier tipo de propiedad"""
    image = models.ImageField(upload_to=property_image_upload_path)
    caption = models.CharField(max_length=200, null=True, blank=True)
    is_main = models.BooleanField(default=False)  # Imagen principal
    order = models.PositiveIntegerField(default=0)  # Orden de visualización

    # Campos para relación genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f"Image for {self.content_object}"


class PropertyDocument(models.Model):
    """Modelo para documentos relacionados con propiedades"""
    DOCUMENT_TYPES = [
        ('contract', 'Contrato'),
        ('deed', 'Escritura'),
        ('identification', 'Identificación'),
        ('proof_income', 'Comprobante de Ingresos'),
        ('other', 'Otro'),
    ]

    document = models.FileField(upload_to='properties/documents/')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='other')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    # Campos para relación genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_document_type_display()}"


class HouseForSale(models.Model):
    title = models.CharField(max_length=120, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    nghood = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    selling_cost = models.IntegerField(null=True, blank=True)
    infonavit = models.BooleanField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def images(self):
        """Retorna todas las imágenes relacionadas"""
        return PropertyImage.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id
        )

    @property
    def main_image(self):
        """Retorna la imagen principal"""
        return self.images.filter(is_main=True).first()

    @property
    def documents(self):
        """Retorna todos los documentos relacionados"""
        return PropertyDocument.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id
        )

    def __str__(self):
        return self.title or f"Casa en {self.street}"


class HouseForRent(models.Model):
    title = models.CharField(max_length=120, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    nghood = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    rent_cost = models.IntegerField(null=True, blank=True)
    garage = models.BooleanField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.FloatField(null=True, blank=True)
    minisplits = models.IntegerField(null=True, blank=True)
    included_services = models.CharField(max_length=200, null=True, blank=True)
    petfriendly = models.BooleanField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    patio = models.BooleanField(null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def images(self):
        """Retorna todas las imágenes relacionadas"""
        return PropertyImage.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id
        )

    @property
    def main_image(self):
        """Retorna la imagen principal"""
        return self.images.filter(is_main=True).first()

    @property
    def documents(self):
        """Retorna todos los documentos relacionados"""
        return PropertyDocument.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id
        )

    def __str__(self):
        return self.title or f"Casa en {self.street}"

    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1NjA1NjQ1MiwiaWF0IjoxNzU1OTcwMDUyLCJqdGkiOiJlMDgyMzg1OTRkNDU0ZWFjYjYwNjc5NTA3NTUyN2ZiOCIsInVzZXJfaWQiOiIxIn0.6OU8f35sAABwCGf8LTtKxIqTWhaix62qQWjgi8tLYhY",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU1OTcwMzUyLCJpYXQiOjE3NTU5NzAwNTIsImp0aSI6IjczZTk0MWU5M2UyYzQ3ZjRhNzZiYmExM2I2YTU5NmMyIiwidXNlcl9pZCI6IjEifQ.AmO6pBRk9zq-rb2jyQT_G-55zz3I4f42bQOa7PjwOlU"
    }