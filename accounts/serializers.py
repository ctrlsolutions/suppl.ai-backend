from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from .models import CustomUser
from decouple import config

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        
        return {"username": user.username}  # Only return username

class ManagerAccountSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get("token")

        if token != config('MANAGER_ACC_TOKEN'):
            raise serializers.ValidationError("Invalid token.")
        
        return {"status": True}
