from django.shortcuts import render, redirect 
from rest_framework import generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.orders.serializers import OrderCreateSerializer
from apps.orders.models import Order, OrderItem
from apps.menu.models import MenuItem
from django.db import transaction


class OrdersView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    
    def post(self, request):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            order = Order.objects.create(
                user = request.user
            )

            for item_data in serializer.validated_data["items"]:
                menu_item = MenuItem.objects.get(pk=item_data["menu_item_id"])

                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=item_data["quantity"]
                )

            return Response({"order_id" : order.id}, status=status.HTTP_201_CREATED)