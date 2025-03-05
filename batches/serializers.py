from rest_framework import serializers
from .models import HealthCheck, Batch
from .models import BatchProduce

class HealthCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCheck
        fields = '__all__'


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'


class BatchProduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchProduce
        fields = '__all__'

# class PredictSerializer(serializers.ModelSerializer):
#     file = serializers.FileField(required=True)  # This will accept the file for processing.

#     class Meta:
#         model = HealthCheck
#         fields = ["file"]


# class PredictSerializer(serializers.Serializer):  
#     file = serializers.FileField()

#     def create(self, validated_data):
#         # Do not create an instance, just return validated data
#         return validated_data

class PredictSerializer(serializers.Serializer):  
    file = serializers.FileField()