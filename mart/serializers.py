from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = users
        fields = ["pk","password","email","username","first_name","last_name","phone","is_active","is_staff","date_joined"]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True}
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value

    def validate_email(self, value):
        if users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        if users.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_phone(self, value):
        if users.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone number already exists")
        return value

    def create(self, validated_data):
        user = users.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

        def validate_product(self, value):
            if users.objects.filter(name=value).exists():
                raise serializers.ValidationError("Product already exists")
            return value


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_Owner
        fields = '__all__'


class Cart_detailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_detail
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
