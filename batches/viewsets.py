from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from .models import HealthCheck, Batch
from .models import BatchProduce
from .serializers import BatchSerializer
from django.http import JsonResponse
from django.db.models import F
from django.db.models import Sum


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
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def wasted_stock(self, request):
        totalwasteditems = BatchProduce.objects.filter(is_spoiled=True).aggregate(Sum("left_in_stock"))["left_in_stock__sum"] or 0
        print(totalwasteditems)
        return Response({"wasted": totalwasteditems})
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def produce_count(self, request):
        totalproduce = BatchProduce.objects.count()
        print(totalproduce)
        return Response({"total": totalproduce})
    

class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def get_batches(self, request):
        batches = self.get_queryset()
        serializer = self.get_serializer(batches, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def add_batch(self, request):
        pass

    @action(detail=False, methods=['patch'], permission_classes=[AllowAny])
    def set_batch_manager(self, request):
        pass



    
    