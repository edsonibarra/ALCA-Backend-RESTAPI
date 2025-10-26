from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.pagination import PageNumberPagination
from owner.models import BaseOwner, Owner


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseOwner
        fields = "__all__"


class OwnerPagination(PageNumberPagination):
    page_size = 10  # Permitir hasta 1000 owners por página
    page_size_query_param = 'page_size'
    max_page_size = 10


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = BaseOwner.objects.all().order_by("name")
    serializer_class = OwnerSerializer
    pagination_class = OwnerPagination
