from rest_framework import serializers
from .models import Cars, Complect


class ComplectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complect
        fields = '__all__'


class CarsSerializer(serializers.ModelSerializer):
    formatted_price = serializers.SerializerMethodField()
    formatted_mileage = serializers.SerializerMethodField()

    class Meta:
        model = Cars
        fields = '__all__'

    def get_formatted_price(self, obj):
        return obj.formatted_price()

    def get_formatted_mileage(self, obj):
        return obj.formatted_mileage()
