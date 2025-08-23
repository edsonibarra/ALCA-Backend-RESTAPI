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

    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'image_url', 'caption', 'is_main', 'order', 'created_at']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class HouseForSaleSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    main_image = PropertyImageSerializer(read_only=True)
    # documents = PropertyDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = HouseForSale
        fields = '__all__'