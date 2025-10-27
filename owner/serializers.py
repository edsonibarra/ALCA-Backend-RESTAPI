from rest_framework import serializers

from owner.models import BaseOwner


class BaseOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseOwner
        fields = "__all__"