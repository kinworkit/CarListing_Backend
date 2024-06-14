from rest_framework import serializers
from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Creates a new user.
    Email, phone, name and password are required.
    Returns a JSON web token
    """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone', 'password', 'token')

    def validate(self, data):
        if 'email' not in data and 'phone' not in data:
            raise serializers.ValidationError("Email or phone is required.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        if 'email' in validated_data:
            email = validated_data.pop('email')
            return CustomUser.objects.create_user(email=email, password=password, **validated_data)
        elif 'phone' in validated_data:
            phone = validated_data.pop('phone')
            return CustomUser.objects.create_user(phone=phone, password=password, **validated_data)


class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(required=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email_or_phone = data.get('email_or_phone', None)
        password = data.get('password', None)

        if not email_or_phone:
            raise serializers.ValidationError('Email or phone is required.')

        user = None

        try:
            # Try authenticate by email address
            if '@' in email_or_phone:
                print("Trying to authenticate with email...")
                user = CustomUser.objects.get(email=email_or_phone)
            else:
                # Try authenticate by number
                print("Trying to authenticate with phone...")
                user = CustomUser.objects.get(phone=email_or_phone)
        except CustomUser.DoesNotExist:
            print("User not found.")
            raise serializers.ValidationError('Invalid credentials.')

        if not user.check_password(password):
            print("Invalid password.")
            raise serializers.ValidationError('Invalid credentials.')

        if not user.is_active:
            print("User is not active.")
            raise serializers.ValidationError('This user has been deactivated.')

        data['user'] = user
        print("Authentication successful.")
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'phone')