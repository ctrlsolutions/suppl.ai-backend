from rest_framework import serializers
from .models import HealthCheck, Batch

class HealthCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCheck
        fields = '__all__'


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'
