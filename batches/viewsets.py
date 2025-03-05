from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from .models import HealthCheck, Batch
from .models import BatchProduce
from .serializers import BatchSerializer
from .serializers import BatchProduceSerializer, PredictSerializer
from django.http import JsonResponse
from django.db.models import F
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from inference_sdk import InferenceHTTPClient
from PIL import Image
import io
import base64 

from rest_framework.decorators import action
from rest_framework import status
from django.core.files.storage import default_storage

# Initialize Roboflow API Client
CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="TRxsXEBYL63UjS4LbQMk"
)

class PredictView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = PredictSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data.get('file')

            # Read image and convert to base64
            image = Image.open(io.BytesIO(file.read()))
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="JPEG")
            image_bytes.seek(0)
            image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')  # ✅ Convert to Base64

            # Send base64 image to Roboflow API
            try:
                result = CLIENT.infer(image_base64, model_id="food-spoilage-status-axom2/7")
            except Exception as e:
                return Response({"error": str(e)}, status=500)

            predictions = result.get("predictions", [])
            response_data = [{"food": pred.get("class", "Unknown"), "confidence": pred.get("confidence", 0) * 100} for pred in predictions]

            return Response({"predictions": response_data}, status=200)

        return Response(serializer.errors, status=400)


class BatchProduceViewSet(viewsets.ModelViewSet):
    queryset = BatchProduce.objects.all()
    serializer_class = BatchProduceSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def get_produces(self, request):
        produces = self.get_queryset()
        serializer = self.get_serializer(produces, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def add_produce(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['patch'], permission_classes=[AllowAny])
    def update_health(self, request, pk=None):
        try:
            batch_produce = self.get_queryset().get(pk=pk)
            prediction = request.data.get("prediction", None)

            if not prediction:
                return Response({"error": "Prediction is required"}, status=400)

            # Set health status based on prediction
            if "fresh" in prediction.lower():
                batch_produce.health_on_arrival = "Average"
            elif "spoiled" in prediction.lower():
                batch_produce.health_on_arrival = "Bad"
            else:
                return Response({"error": "Invalid prediction"}, status=400)

            batch_produce.save()

            return Response({
                "message": "Health status updated successfully",
                "health_status": batch_produce.health_on_arrival
            })

        except BatchProduce.DoesNotExist:
            return Response({"error": "BatchProduce not found"}, status=404)
        
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
        print("oten")
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



    
    