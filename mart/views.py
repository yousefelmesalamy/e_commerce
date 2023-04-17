from _testcapi import raise_exception
from django.shortcuts import render
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics,mixins,viewsets
from rest_framework.response import Response
from rest_framework import status, filters
from django.http.response import JsonResponse
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from django.shortcuts import get_object_or_404
from django.http import Http404
from .permissons import *
import requests

from rest_framework.decorators import action


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
            })
        else:
            return Response({"Response": "username or password was incorrect"}, status=status.HTTP_401_UNAUTHORIZED)


# U S E R  C . B . V

class User_list_CBV(APIView):
    permission_classes = [UserPermission]

    def get(self, request, pk=None):
        if pk:
            obj = self.get_object(pk=pk)
            serializer = UserSerializer(obj)
        else:

            obj = users.objects.all()
            serializer = UserSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['get'])
    def get_object(self, pk):
        try:
            return users.objects.get(pk=pk)
        except users.DoesNotExist:
            raise Http404

    def retrieve(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class User_pk_CBV(APIView):
#     permission_classes = [UserPermission]
    #
    # def get_object(self, pk):
    #     try:
    #         return users.objects.get(pk=pk)
    #     except users.DoesNotExist:
    #         raise Http404
    #
    # def get(self,request,pk):
    #     user=self.get_object(pk)
    #     serializer=UserSerializer(user)
    #     return Response(serializer.data)
    #
    # def put(self, request, pk):
    #     user=self.get_object(pk)
    #     serializer=UserSerializer(user,data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self,request,pk):
    #     user=self.get_object(pk)
    #     user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #

# P R O D U C T  C . B . V
class Product_list_CBV(APIView):
    permission_classes = [UserPermission]

    def get(self,request):
        product = Products.objects.all()
        serializer = ProductSerializer(product,many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)

class Product_pk_CBV(APIView):
    permission_classes = [UserPermission]

    def get_object(self, pk):
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        product=self.get_object(pk)
        serializer=ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product=self.get_object(pk)
        serializer=ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        product=self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# C A R T  C . B . V
class Cart_Owner_list_CBV(APIView):
    permission_classes = [UserPermission]

    def get(self,request):
        cart=Cart_Owner.objects.all()
        serializer=CartSerializer(cart,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


class Cart_Owner_pk_CBV(APIView):
    permission_classes = [UserPermission]

    def get_object(self, pk):
        try:
            return Cart_Owner.objects.get(pk=pk)
        except Cart_Owner.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        cart=self.get_object(pk)
        serializer=CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, pk):
        cart=self.get_object(pk)
        serializer=CartSerializer(cart,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        cart=self.get_object(pk)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Cart_Detail_list_CBV(APIView):
    permission_classes = [UserPermission]

    def get(self,request):
        cartdetail=Cart_detail.objects.all()
        serializer=Cart_detailSerializer(cartdetail,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=Cart_detailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


class Cart_Detail_pk_CBV(APIView):
    permission_classes = [UserPermission]

    def get_object(self, pk):
        try:
            return Cart_detail.objects.get(pk=pk)
        except Cart_detail.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        cartdetail = self.get_object(pk)
        serializer = Cart_detailSerializer(cartdetail)
        return Response(serializer.data)

    def put(self, request, pk):
        cartdetail = self.get_object(pk)
        serializer = Cart_detailSerializer(cartdetail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        cartdetail = self.get_object(pk)
        cartdetail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Order_list_CBV(APIView):
    permission_classes = [UserPermission]

    def get(self,request):
        checkout=Order.objects.all()
        serializer=OrderSerializer(checkout,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


class Order_pk_CBV(APIView):
    permission_classes = [UserPermission]

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        checkout = self.get_object(pk)
        serializer = Check_outSerializer(checkout)
        return Response(serializer.data)

    def put(self, request, pk):
        checkout = self.get_object(pk)
        serializer = Check_outSerializer(checkout,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        checkout = self.get_object(pk)
        checkout.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class User_viewset (viewsets.ModelViewSet):
    queryset=users.objects.all()
    serializer_class=UserSerializer
    permission_classes = [UserPermission]


# #filter of product function
# @api_view(['GET'])
# def find_product(request):
#     product=Products.objects.filter(
#         name=request.data['name']
#     )
#     serializer=ProductSerializer(product,many=True)
#     return Response (serializer.data)

class Product_viewset(viewsets.ModelViewSet):
    queryset=Products.objects.all()
    serializer_class=ProductSerializer
    permission_classes = [UserPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']


class Cart_Owner_Viewset (viewsets.ModelViewSet):
    queryset = Cart_Owner.objects.all()
    serializer_class = CartSerializer
    permission_classes = [UserPermission]


class Cart_Detail_Viewset(viewsets.ModelViewSet):
    queryset = Cart_detail.objects.all()
    serializer_class = Cart_detailSerializer
    permission_classes = [UserPermission]


class Check_Out_Viewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [UserPermission]
