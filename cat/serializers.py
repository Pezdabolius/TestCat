from rest_framework import serializers
from .models import Kitten


class KittenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitten
        fields = '__all__'
