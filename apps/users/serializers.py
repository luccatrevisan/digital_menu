from rest_framework import serializers
from apps.users.models import CustomUser
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone_number", "password"]

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username muito curto.")
        return value
 
    def create(self, validated_data): 
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"]
        )

        return user