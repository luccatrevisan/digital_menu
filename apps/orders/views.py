from django.shortcuts import render 
from rest_framework import generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.orders.serializers import OrderCreateSerializer
from apps.orders.services.create_order import create_order
from django.core.exceptions import ValidationError


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
                items_data = serializer.validated_data["items"]
            )
        
        except ValidationError as e:
            return Response(
                {"detail" : e.message},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"order_id" : order.id}, status=status.HTTP_201_CREATED)
        

def order_success(request):
    return render(request, "orders/order_success.html")