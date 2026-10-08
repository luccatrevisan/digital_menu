from django.shortcuts import render 
from rest_framework import generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.orders.serializers import OrderCreateSerializer
from apps.orders.services.create_order import create_order
from django.core.exceptions import ValidationError as DjangoValidationError
from apps.orders.exceptions import InsufficientStockError


class OrdersView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer


    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = create_order(
                user = request.user,
                items_data = serializer.validated_data["items"],
                address_id = serializer.validated_data["address_id"],
            )
            
        except InsufficientStockError as error:
            return Response(
                {
                    "items": {
                        "message": str(error),
                        "menu_item": error.menu_item_name,
                        "remaining": error.available_quantity,
                        "code": "stock_unavailable",
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        except DjangoValidationError as error:
            return Response(
                {
                    "message": error.messages[0],
                    "code": getattr(error, "code", None) or "invalid_order",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"order_id" : order.id}, status=status.HTTP_201_CREATED)


def checkout(request):
    return render(request, "orders/checkout.html")


def order_success(request):
    return render(request, "orders/order_success.html")