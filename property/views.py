from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.contenttypes.models import ContentType

from .models import HouseForSale, PropertyImage
from .serializers import PropertyImageUploadSerializer, PropertyImageSerializer, HouseForSaleSerializer


class HouseForSaleViewSet(viewsets.ModelViewSet):
    queryset = HouseForSale.objects.all()
    serializer_class = HouseForSaleSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_images(self, request, pk=None):
        """
        Upload multiple images to a HouseForSale
        Endpoint: POST /houses-for-sale/{id}/upload_images/
        """
        house = self.get_object()
        files = request.FILES.getlist("images")  # multiple files

        if not files:
            return Response({"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST)

        created_images = []
        content_type = ContentType.objects.get_for_model(HouseForSale)

        for img_file in files:
            serializer = PropertyImageUploadSerializer(
                data={
                    "image": img_file,
                    "content_type": "house_for_sale",
                    "object_id": house.id,
                    "is_main": request.data.get("is_main", False),
                    "caption": request.data.get("caption", ""),
                    "order": request.data.get("order", 0),
                },
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            image = serializer.save()
            created_images.append(image)

        return Response(
            PropertyImageSerializer(created_images, many=True, context={"request": request}).data,
            status=status.HTTP_201_CREATED
        )
