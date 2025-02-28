from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from .models import CustomUser, ManagerUser
from .serializers import UserLoginSerializer, ManagerAccountSerializer

class AuthViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Handles user login"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            user = CustomUser.objects.get(username=username)
            update_last_login(None, user)  # Update last login timestamp
            
            # Check if user is a manager (proxy model check)
            is_manager = isinstance(user, ManagerUser)

            return Response(
                {
                    "success": True,
                    "user": {
                        "username": user.username,
                        "branch": user.branch,
                        "role": "Manager" if is_manager else "User",
                    },
                },
                status=status.HTTP_200_OK
            )
        return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def validate_token(self, request):
        serializer = ManagerAccountSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data["status"]:
                return Response({"valid": True})
        return Response({"valid": False})
            
