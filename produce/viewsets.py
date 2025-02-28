from rest_framework import viewsets
from .models import Produce
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from .models import Produce
from .serializers import ProduceSerializer
from django.http import JsonResponse
from django.db.models import F

class ProduceViewSet(viewsets.ModelViewSet):
    queryset = Produce.objects.all()
    serializer_class = ProduceSerializer

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def get_Produces(self, request):
        Producees = self.get_queryset()
        serializer = self.get_serializer(Producees, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def add_Produce(self, request):
        pass