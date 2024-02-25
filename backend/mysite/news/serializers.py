from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import New


class NewSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    text = serializers.CharField(max_length=2000)
    image = serializers.ImageField(max_length=None, required=False, use_url=False)
    
    class Meta:
        model = New
        fields = '__all__'