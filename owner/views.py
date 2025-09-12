from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.pagination import PageNumberPagination

from owner.models import Owner

# Create your views here.
# class HouseForSaleViewSet(viewsets.ModelViewSet):
#     queryset = HouseForSale.objects.all()
#     serializer_class = HouseForSaleSerializer


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = "__all__"

class OwnerPagination(PageNumberPagination):
    page_size = 1000  # Permitir hasta 1000 owners por página
    page_size_query_param = 'page_size'
    max_page_size = 1000

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by("name")
    serializer_class = OwnerSerializer
    pagination_class = OwnerPagination