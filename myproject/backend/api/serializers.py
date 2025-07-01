# backend/api/serializers.py
from rest_framework import serializers
from .models import ProdukHukum, LogUpdate
from .models import DataPotensi

class ProdukHukumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdukHukum
        fields = '__all__'

class LogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogUpdate
        fields = '__all__'

class DataPotensiSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPotensi
        fields = '__all__'