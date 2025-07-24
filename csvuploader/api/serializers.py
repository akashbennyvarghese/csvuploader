from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'age']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Name must be a string.")
        return value

    def validate_email(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Email must be provided.")
        return value

    def validate_age(self, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise serializers.ValidationError("Age must be an integer.")
        if not (0 <= value <= 120):
            raise serializers.ValidationError("Age must be between  0 and 120.")
        return value
