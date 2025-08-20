from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

# -------------------- LOGIN --------------------
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = User.objects(email=attrs['email']).first()
        if not user or not user.check_password(attrs['password']):
            raise serializers.ValidationError("Invalid credentials.")
        attrs['user'] = user
        return attrs


# -------------------- CREATE --------------------
class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    mobile_no = serializers.CharField(required=True)
    city = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=('management', 'staff', 'guest'), default='guest')

    def validate_email(self, value):
        if User.objects(email=value).first():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User(**validated_data)
        user.save()
        return user


# -------------------- UPDATE --------------------
class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    mobile_no = serializers.CharField(required=False)
    city = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=('management', 'staff', 'guest'), required=False)

    # ❌ Removed email & password from update
    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


# -------------------- LIST --------------------
class UserListSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    mobile_no = serializers.CharField()
    city = serializers.CharField()
    role = serializers.CharField()

    def to_representation(self, instance):
        return instance.to_dict()
