from django.shortcuts import render
from rest_framework import viewsets, serializers

from owner.models import Owner

# Create your views here.
# class HouseForSaleViewSet(viewsets.ModelViewSet):
#     queryset = HouseForSale.objects.all()
#     serializer_class = HouseForSaleSerializer


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = "__all__"

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by("name")
    serializer_class = OwnerSerializer