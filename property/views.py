# views.py
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from .models import HouseForSale, PropertyImage
from .serializers import (
    HouseForSaleSerializer,
    PropertyImageSerializer,
    PropertyImageUploadSerializer
)


class HouseForSaleViewSet(viewsets.ModelViewSet):
    queryset = HouseForSale.objects.all()
    serializer_class = HouseForSaleSerializer
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_image(self, request, pk=None):
        """Subir imagen a una casa en venta"""
        house = self.get_object()

        # Si hay una imagen marcada como principal y esta nueva también lo es,
        # desmarcar la anterior
        if request.data.get('is_main') == 'true':
            house.images.filter(is_main=True).update(is_main=False)

        serializer = PropertyImageUploadSerializer(data={
            **request.data,
            'content_type': 'house_for_sale',
            'object_id': house.id
        }, context={'request': request})

        if serializer.is_valid():
            image = serializer.save()
            return Response(PropertyImageSerializer(image, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_image(self, request, pk=None):
        """Eliminar imagen específica"""
        house = self.get_object()
        image_id = request.query_params.get('image_id')

        if not image_id:
            return Response({'error': 'image_id es requerido'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            image = house.images.get(id=image_id)
            image.delete()
            return Response({'message': 'Imagen eliminada'}, status=status.HTTP_200_OK)
        except PropertyImage.DoesNotExist:
            return Response({'error': 'Imagen no encontrada'},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'])
    def set_main_image(self, request, pk=None):
        """Establecer imagen principal"""
        house = self.get_object()
        image_id = request.data.get('image_id')

        if not image_id:
            return Response({'error': 'image_id es requerido'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Desmarcar todas las imágenes como principales
            house.images.update(is_main=False)
            # Marcar la nueva como principal
            image = house.images.get(id=image_id)
            image.is_main = True
            image.save()

            return Response({'message': 'Imagen principal actualizada'},
                            status=status.HTTP_200_OK)
        except PropertyImage.DoesNotExist:
            return Response({'error': 'Imagen no encontrada'},
                            status=status.HTTP_404_NOT_FOUND)
