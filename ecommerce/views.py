from django.shortcuts import get_object_or_404
from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer, CartSerializer
from .models import Cart, Order


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
        orders = Order.objects.filter(user=request.user)
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
    

@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def cart_list(request):
    if request.method == 'GET':
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        count_cart = cart_items.count()
        if count_cart > 0:
            serializer = CartSerializer(cart_items, many=True)
            return Response({
                'Data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'Empty': 'Your cart is empty now!'
            }, status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def cart_detail(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk)
    if request.method == 'GET':
        serializer = CartSerializer(cart_item)
        return Response(serializer.data)
    
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        order_id = request.data.get('order')
        # Retrieve the order object
        order = get_object_or_404(Order, pk=order_id)

        # Check if the order already exists in the user's cart
        existing_cart_item = Cart.objects.filter(user=user, order=order).first()

        if existing_cart_item:
            # If the order already exists in the cart, you can update the quantity or perform any other actions
            return Response({"Message": "Item already exists in the cart"}, status=status.HTTP_409_CONFLICT)
        else:
            # If the order doesn't exist in the cart, create a new cart item
            cart_item = Cart.objects.create(user=user, order=order)
            serializer = CartSerializer(cart_item)
            return Response({
                'Created': 'The Cart created successfully and here is your data',
                'Data': serializer.data
            }, status=status.HTTP_201_CREATED)

@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def cart_item_delete(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk)
    # Check if the user has permission to delete this cart item
    if cart_item.user != request.user:
        return Response({"error": "You do not have permission to delete this cart item"}, status=status.HTTP_403_FORBIDDEN)

    # Perform delete operation
    cart_item.delete()

    return Response({"message": "Cart item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)