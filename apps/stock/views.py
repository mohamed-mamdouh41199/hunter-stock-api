from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import StockItem
from .serializers import StockItemSerializer
from bson import ObjectId


class StockItemViewSet(viewsets.ViewSet):
    """
    ViewSet for managing stock items.
    Provides CRUD operations for hunter's stock.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """List all stock items for the authenticated user"""
        items = StockItem.objects(hunter_id=request.user.id)
        serializer = StockItemSerializer(items, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Create a new stock item"""
        serializer = StockItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Retrieve a specific stock item"""
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            serializer = StockItemSerializer(item)
            return Response(serializer.data)
        except StockItem.DoesNotExist:
            return Response({'error': 'Stock item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        """Update a stock item"""
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            serializer = StockItemSerializer(item, data=request.data, partial=False, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StockItem.DoesNotExist:
            return Response({'error': 'Stock item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        """Partially update a stock item"""
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            serializer = StockItemSerializer(item, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StockItem.DoesNotExist:
            return Response({'error': 'Stock item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        """Delete a stock item"""
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StockItem.DoesNotExist:
            return Response({'error': 'Stock item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def my_stock(self, request):
        """Get all stock items for the authenticated user"""
        items = StockItem.objects(hunter_id=request.user.id)
        serializer = StockItemSerializer(items, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increase_quantity(self, request, pk=None):
        """Increase quantity of a stock item"""
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            amount = int(request.data.get('amount', 1))
            item.quantity += amount
            item.save()
            serializer = StockItemSerializer(item)
            return Response(serializer.data)
        except StockItem.DoesNotExist:
            return Response({'error': 'Stock item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def decrease_quantity(self, request, pk=None):
        """Decrease quantity of a stock item"""
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            amount = int(request.data.get('amount', 1))
            item.quantity = max(0, item.quantity - amount)
            item.save()
            serializer = StockItemSerializer(item)
            return Response(serializer.data)
        except StockItem.DoesNotExist:
            return Response({'error': 'Stock item not found'}, status=status.HTTP_404_NOT_FOUND)


