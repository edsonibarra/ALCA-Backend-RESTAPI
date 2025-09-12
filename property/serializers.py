# serializers.py
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import HouseForSale, HouseForRent, PropertyImage


class PropertyImageUploadSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()
    object_id = serializers.IntegerField()

    class Meta:
        model = PropertyImage
        fields = ['image', 'caption', 'is_main', 'order', 'content_type', 'object_id']

    def create(self, validated_data):
        content_type_str = validated_data.pop('content_type')

        # Mapeo de strings a modelos
        model_mapping = {
            'house_for_sale': HouseForSale,
            'house_for_rent': HouseForRent,
        }

        if content_type_str not in model_mapping:
            raise serializers.ValidationError("Tipo de contenido no válido")

        model_class = model_mapping[content_type_str]
        content_type = ContentType.objects.get_for_model(model_class)
        validated_data['content_type'] = content_type

        return super().create(validated_data)



class PropertyImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    secure_url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'image_url', 'secure_url', 'caption', 'is_main', 'order', 'created_at']

    def get_image_url(self, obj):
        """
        Deprecated: Use secure_url instead.
        This field is kept for backward compatibility.
        """
        return self.get_secure_url(obj)

    def get_secure_url(self, obj):
        """
        Generate a secure presigned URL for the image
        """
        if obj.image:
            # Get expiration time from context or use default (1 hour)
            expiration = self.context.get('url_expiration', 3600)
            return obj.get_secure_url(expiration)
        return None


class HouseForSaleSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    main_image = PropertyImageSerializer(read_only=True)
    # documents = PropertyDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = HouseForSale
        fields = '__all__'


class HouseForRentSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    main_image = PropertyImageSerializer(read_only=True)

    class Meta:
        model = HouseForRent
        fields = '__all__'