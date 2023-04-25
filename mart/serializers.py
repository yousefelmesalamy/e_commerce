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
    stock_status = serializers.SerializerMethodField()
    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'condition', 'description', 'qty', 'barcode', 'date_of_entry', 'valid_to', 'expired', 'stock_status', 'image']

    def get_stock_status(self, obj):
        return obj.stock()

        def validate_product(self, value):
            if users.objects.filter(name=value).exists():
                raise serializers.ValidationError("Product already exists")
            return value


class CartOwnerSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.username')
    class Meta:
        model = Cart_Owner
        fields = ['id', 'username']


class Cart_detailSerializer(serializers.ModelSerializer):
    coast_of_products = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='products.name')
    cart_owner = serializers.CharField(source='cart_owner.user.username')

    class Meta:
        model = Cart_detail
        fields = ['product_name', 'cart_owner', 'coast_of_products']

    def get_coast_of_products(self,obj):
        return obj.coast_of_product()


class OrderSerializer(serializers.ModelSerializer):
    cart_owner = serializers.CharField(source='cart.user.username')
    num_of_products = serializers.SerializerMethodField()
    coast_of_products = serializers.SerializerMethodField()
    deliver_to = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['cart_owner', 'num_of_products', 'coast_of_products', 'deliver_to']

    def get_num_of_products(self,obj):
        return obj.num_of_products()

    def get_coast_of_products(self,obj):
        return obj.coast_of_products()

    def get_deliver_to(self,obj):
        return obj.deliver_to()

