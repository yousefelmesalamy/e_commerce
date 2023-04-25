from django.urls import path, include
from django.http import Http404
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('users', User_viewset)
router.register('products', Product_viewset)
router.register('cart/owner', Cart_Owner_Viewset)
router.register('cart/detail', Cart_Detail_Viewset)
router.register('checkout', Order_Viewset)



urlpatterns = [

    path('rest/viewsets/', include(router.urls)),

    # 1.1 GET & POST REST_FRAMEWORK CLASS BASED VIEW APIView FOR USER
    path('rest/user/', User_list_CBV.as_view()),

    # 1.2 GET PUT DELETE from REST_FRAMEWORK class BASED VIEW APIView FOR USER
    path('rest/user/<int:pk>/', User_list_CBV.as_view(), name='mark-as-read'),

    # 2.1 GET & POST REST_FRAMEWORK CLASS BASED VIEW APIView FOR PRODUCT
    path('rest/product/', Product_list_CBV.as_view()),

    # 2.2 GET PUT DELETE from REST_FRAMEWORK class BASED VIEW APIView FOR PRODUCT
    path('rest/product/<int:pk>', Product_pk_CBV.as_view()),

    # 3.1 GET & POST REST_FRAMEWORK CLASS BASED VIEW APIView FOR CART
    path('rest/cart/owner', Cart_Owner_list_CBV.as_view()),

    # 3.2 GET PUT DELETE from REST_FRAMEWORK class BASED VIEW APIView FOR CART
    path('rest/cart/owner/<int:pk>', Cart_Owner_pk_CBV.as_view()),

    # 3.1 GET & POST REST_FRAMEWORK CLASS BASED VIEW APIView FOR CART
    path('rest/cart/detail/', Cart_Detail_list_CBV.as_view()),

    # 3.2 GET PUT DELETE from REST_FRAMEWORK class BASED VIEW APIView FOR CART
    path('rest/cart/detail/<int:pk>', Cart_Detail_pk_CBV.as_view()),

    # 3.1 GET & POST REST_FRAMEWORK CLASS BASED VIEW APIView FOR CART
    path('rest/order/', Order_list_CBV.as_view()),

    # 3.2 GET PUT DELETE from REST_FRAMEWORK class BASED VIEW APIView FOR CART
    path('rest/order/<int:pk>', Order_pk_CBV.as_view()),
    #4 find product filter
    # path('findproduct/',find_product),


]

