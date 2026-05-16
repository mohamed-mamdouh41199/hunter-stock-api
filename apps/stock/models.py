from mongoengine import Document, StringField, IntField, DateTimeField, ReferenceField
from django.contrib.auth.models import User as DjangoUser
import datetime


class StockItem(Document):
    """Model to represent a hunter's stock item"""
    
    name = StringField(required=True, max_length=200)
    quantity = IntField(default=0)
    item_type = StringField(required=True, max_length=100)
    hunter_id = IntField(required=True)  # Store Django User ID
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    
    meta = {
        'collection': 'stock_items',
        'ordering': ['-created_at'],
        'indexes': [
            'hunter_id',
            '-created_at'
        ]
    }
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(StockItem, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.quantity})"
    
    @property
    def hunter(self):
        """Get the Django user associated with this stock item"""
        try:
            return DjangoUser.objects.get(id=self.hunter_id)
        except DjangoUser.DoesNotExist:
            return None


