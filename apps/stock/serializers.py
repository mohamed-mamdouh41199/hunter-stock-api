from rest_framework import serializers
from .models import StockItem


class StockItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200, required=True)
    quantity = serializers.IntegerField(default=0)
    item_type = serializers.CharField(max_length=100, required=True)
    hunter_id = serializers.IntegerField(read_only=True)
    hunter_username = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def get_hunter_username(self, obj):
        hunter = obj.hunter
        return hunter.username if hunter else None
    
    def create(self, validated_data):
        validated_data['hunter_id'] = self.context['request'].user.id
        stock_item = StockItem(**validated_data)
        stock_item.save()
        return stock_item
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.item_type = validated_data.get('item_type', instance.item_type)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Convert MongoDB document to dictionary"""
        return {
            'id': str(instance.id),
            'name': instance.name,
            'quantity': instance.quantity,
            'item_type': instance.item_type,
            'hunter_id': instance.hunter_id,
            'hunter_username': instance.hunter.username if instance.hunter else None,
            'created_at': instance.created_at.isoformat() if instance.created_at else None,
            'updated_at': instance.updated_at.isoformat() if instance.updated_at else None,
        }

