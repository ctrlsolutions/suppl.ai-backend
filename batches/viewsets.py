from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from .models import HealthCheck
from .models import BatchProduce
from .serializers import HealthCheckSerializer
from django.http import JsonResponse
from django.db.models import F


class DashboardViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def near_exp(self, request):
        averageitems = HealthCheck.objects.filter(health_status='average').count()
        # print(averageitems)
        return Response({"avg": averageitems})
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def low_stock(self, request):
        lowstockitems = BatchProduce.objects.filter(left_in_stock__lte=F("initial_stock")*0.25).count()
        print(lowstockitems)
        return Response({"low": lowstockitems})
    
    
    