from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from .models import HealthCheck
from .serializers import HealthCheckSerializer
from django.http import JsonResponse


class AverageHealthCheckView(viewsets.ModelViewSet):
    serializer_class = HealthCheckSerializer

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def get(self, request):
        averageitems = HealthCheck.objects.filter(health_status='average').count()
        # print(averageitems)
        return Response({"avg": averageitems})
    
    