from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType
from owner.models import Owner
from backend.storage_backends import PrivateMediaStorage


def property_image_upload_path(instance, filename):
    """Función para definir la ruta de subida de imágenes"""
    import uuid
    from datetime import datetime
    
    # Obtiene la extensión del archivo
    ext = filename.split('.')[-1]
    
    # Crea un nombre único basado en el modelo, ID y timestamp
    model_name = instance.content_object._meta.model_name
    object_id = instance.object_id
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    
    # Nuevo nombre de archivo único
    new_filename = f"{timestamp}_{unique_id}.{ext}"
    
    return f'properties/{model_name}/{object_id}/{new_filename}'


class PropertyImage(models.Model):
    """Modelo genérico para manejar imágenes de cualquier tipo de propiedad"""
    image = models.ImageField(
        upload_to=property_image_upload_path,
        storage=PrivateMediaStorage()
    )
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
    
    def get_secure_url(self, expiration=3600):
        """
        Generate a secure presigned URL for this image
        
        Args:
            expiration (int): Time in seconds for the URL to remain valid
        
        Returns:
            str: Presigned URL or None if error
        """
        if self.image:
            from backend.storage_backends import S3ImageService
            s3_service = S3ImageService()
            return s3_service.generate_presigned_url(self.image.name, expiration)
        return None


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
    estatus = models.CharField(max_length=120, null=True, blank=True)
    cochera = models.IntegerField(null=True, blank=True)
    baths = models.FloatField(null=True, blank=True)
    patio = models.BooleanField(null=True, blank=True)
    beds = models.IntegerField(null=True, blank=True)
    minisplits = models.IntegerField(null=True, blank=True)
    construccion = models.FloatField(null=True, blank=True)
    superficie = models.FloatField(null=True, blank=True)
    servicios = models.CharField(max_length=120, null=True, blank=True)
    metodo_de_pago = models.CharField(max_length=120, null=True, blank=True)
    negociable = models.BooleanField(null=True, blank=True)


    @property
    def images(self):
        """Retorna todas las imágenes relacionadas"""
        return PropertyImage.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id
        )

    def __str__(self):
        return str(self.title)


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

    def __str__(self):
        return self.title
