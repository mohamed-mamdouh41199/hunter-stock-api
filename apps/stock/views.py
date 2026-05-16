from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import StockItem
from .serializers import StockItemSerializer
from .utils import ApiResponse, ResponseMessages


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
        return ApiResponse.success(
            data=serializer.data,
            message=ResponseMessages.STOCK_LIST_SUCCESS
        )
    
    def create(self, request):
        """Create a new stock item"""
        serializer = StockItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.created(
                data=serializer.data,
                message=ResponseMessages.STOCK_CREATED
            )
        return ApiResponse.validation_error(
            errors=serializer.errors,
            message=ResponseMessages.VALIDATION_ERROR
        )
    
    def retrieve(self, request, pk=None):
        """Retrieve a specific stock item"""
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            serializer = StockItemSerializer(item)
            return ApiResponse.success(
                data=serializer.data,
                message=ResponseMessages.STOCK_LIST_SUCCESS
            )
        except StockItem.DoesNotExist:
            return ApiResponse.not_found(
                resource="Stock item"
            )
    
    def update(self, request, pk=None):
        """Update a stock item"""
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            serializer = StockItemSerializer(item, data=request.data, partial=False, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return ApiResponse.success(
                    data=serializer.data,
                    message=ResponseMessages.STOCK_UPDATED
                )
            return ApiResponse.validation_error(
                errors=serializer.errors,
                message=ResponseMessages.VALIDATION_ERROR
            )
        except StockItem.DoesNotExist:
            return ApiResponse.not_found(resource="Stock item")
    
    def partial_update(self, request, pk=None):
        """Partially update a stock item"""
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            serializer = StockItemSerializer(item, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return ApiResponse.success(
                    data=serializer.data,
                    message=ResponseMessages.STOCK_UPDATED
                )
            return ApiResponse.validation_error(
                errors=serializer.errors,
                message=ResponseMessages.VALIDATION_ERROR
            )
        except StockItem.DoesNotExist:
            return ApiResponse.not_found(resource="Stock item")
    
    def destroy(self, request, pk=None):
        """Delete a stock item"""
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            item.delete()
            return ApiResponse.no_content(
                message=ResponseMessages.STOCK_DELETED
            )
        except StockItem.DoesNotExist:
            return ApiResponse.not_found(resource="Stock item")
    
    @action(detail=False, methods=['get'])
    def my_stock(self, request):
        """Get all stock items for the authenticated user"""
        items = StockItem.objects(hunter_id=request.user.id)
        serializer = StockItemSerializer(items, many=True)
        return ApiResponse.success(
            data=serializer.data,
            message=ResponseMessages.STOCK_LIST_SUCCESS
        )
    
    @action(detail=True, methods=['post'])
    def increase_quantity(self, request, pk=None):
        """Increase quantity of a stock item"""
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            amount = int(request.data.get('amount', 1))
            item.quantity += amount
            item.save()
            serializer = StockItemSerializer(item)
            return ApiResponse.success(
                data=serializer.data,
                message=ResponseMessages.STOCK_QUANTITY_INCREASED
            )
        except StockItem.DoesNotExist:
            return ApiResponse.not_found(resource="Stock item")
    
    @action(detail=True, methods=['post'])
    def decrease_quantity(self, request, pk=None):
        """Decrease quantity of a stock item"""
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            amount = int(request.data.get('amount', 1))
            item.quantity = max(0, item.quantity - amount)
            item.save()
            serializer = StockItemSerializer(item)
            return ApiResponse.success(
                data=serializer.data,
                message=ResponseMessages.STOCK_QUANTITY_DECREASED
            )
        except StockItem.DoesNotExist:
            return ApiResponse.not_found(resource="Stock item")

