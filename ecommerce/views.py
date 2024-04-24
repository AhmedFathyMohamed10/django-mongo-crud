from django.shortcuts import get_object_or_404
from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from django.contrib.auth.models import User



@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        user = request.user
        serializer = OrderSerializer(data=request.data)
        
        if serializer.is_valid():
            # Check if the product has stock
            product_id = serializer.validated_data.get('product_id')
            quantity = serializer.validated_data.get('quantity')
            if product_id.stock >= quantity:
                # Calculate the total cost
                total_cost = quantity * Decimal(product_id.price)
                serializer.validated_data['total_cost'] = total_cost
                # Update the product stock
                product_id.stock -= quantity
                product_id.save()
                # Save the order
                serializer.save(user=user)
                # Return the response
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise serializers.ValidationError("Insufficient stock!")
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)