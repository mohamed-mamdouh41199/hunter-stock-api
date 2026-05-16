# 🎓 Your views.py - Annotated for Node.js Developer

## This file is: **CONTROLLER + SERVICE LAYER combined!**

```python
# ========================================
# 📦 IMPORTS (like require() in Node.js)
# ========================================
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import StockItem              # ← Like: const StockItem = require('./models/StockItem')
from .serializers import StockItemSerializer  # ← Like: const validator = require('./validators')
from bson import ObjectId


# ========================================
# 🎮 CONTROLLER CLASS
# Node.js equivalent: exports.getAllItems, exports.createItem, etc.
# ========================================
class StockItemViewSet(viewsets.ViewSet):
    """
    This is YOUR CONTROLLER + SERVICE combined!
    
    In Node.js, this would be split into:
    - controllers/stock.controller.js (handles HTTP)
    - services/stock.service.js (business logic)
    """
    
    # 🔐 MIDDLEWARE - Like app.use(authMiddleware)
    permission_classes = [permissions.IsAuthenticated]
    
    # ========================================
    # 📍 ENDPOINT: GET /api/stock/items/
    # Node.js: router.get('/items', controller.list)
    # ========================================
    def list(self, request):
        """
        Node.js equivalent:
        
        exports.getAllItems = async (req, res) => {
            const items = await StockItem.find({ hunterId: req.user.id });
            res.json(items);
        }
        """
        # DATABASE QUERY (like StockItem.find() in Mongoose)
        items = StockItem.objects(hunter_id=request.user.id)
        
        # SERIALIZATION (like DTO transformation)
        serializer = StockItemSerializer(items, many=True)
        
        # RESPONSE (like res.json())
        return Response(serializer.data)
    
    # ========================================
    # 📍 ENDPOINT: POST /api/stock/items/
    # Node.js: router.post('/items', controller.create)
    # ========================================
    def create(self, request):
        """
        Node.js equivalent:
        
        exports.createItem = async (req, res) => {
            const { error, value } = schema.validate(req.body);
            if (error) return res.status(400).json({ error });
            
            const item = new StockItem({ ...value, hunterId: req.user.id });
            await item.save();
            res.status(201).json(item);
        }
        """
        # VALIDATION (like Joi.validate())
        serializer = StockItemSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():  # ← Validation passed
            serializer.save()       # ← Create in database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Validation failed
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # ========================================
    # 📍 ENDPOINT: GET /api/stock/items/:id/
    # Node.js: router.get('/items/:id', controller.getItem)
    # ========================================
    def retrieve(self, request, pk=None):
        """
        pk = Primary Key (like :id parameter in Express)
        
        Node.js equivalent:
        
        exports.getItem = async (req, res) => {
            try {
                const item = await StockItem.findOne({
                    _id: req.params.id,
                    hunterId: req.user.id
                });
                if (!item) return res.status(404).json({ error: 'Not found' });
                res.json(item);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        }
        """
        try:
            # FIND ONE (like StockItem.findOne())
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            serializer = StockItemSerializer(item)
            return Response(serializer.data)
        except StockItem.DoesNotExist:  # ← Like: if (!item)
            return Response({'error': 'Stock item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # ========================================
    # 📍 ENDPOINT: PUT /api/stock/items/:id/
    # Node.js: router.put('/items/:id', controller.updateItem)
    # ========================================
    def update(self, request, pk=None):
        """
        Full update (all fields required)
        
        Node.js equivalent:
        
        exports.updateItem = async (req, res) => {
            const item = await StockItem.findOne({ _id: req.params.id, hunterId: req.user.id });
            if (!item) return res.status(404).json({ error: 'Not found' });
            
            Object.assign(item, req.body);
            await item.save();
            res.json(item);
        }
        """
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            serializer = StockItemSerializer(item, data=request.data, partial=False, context={'request': request})
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StockItem.DoesNotExist:
            return Response({'error': 'Stock item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # ========================================
    # 📍 ENDPOINT: PATCH /api/stock/items/:id/
    # Node.js: router.patch('/items/:id', controller.partialUpdate)
    # ========================================
    def partial_update(self, request, pk=None):
        """
        Partial update (only provided fields)
        partial=True means: only validate fields that are sent
        
        Node.js equivalent: Same as update, but doesn't require all fields
        """
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            serializer = StockItemSerializer(item, data=request.data, partial=True, context={'request': request})
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StockItem.DoesNotExist:
            return Response({'error': 'Stock item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # ========================================
    # 📍 ENDPOINT: DELETE /api/stock/items/:id/
    # Node.js: router.delete('/items/:id', controller.deleteItem)
    # ========================================
    def destroy(self, request, pk=None):
        """
        Node.js equivalent:
        
        exports.deleteItem = async (req, res) => {
            const item = await StockItem.findOne({ _id: req.params.id, hunterId: req.user.id });
            if (!item) return res.status(404).json({ error: 'Not found' });
            
            await item.remove();
            res.status(204).send();
        }
        """
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            item.delete()  # ← Like item.remove() in Mongoose
            return Response(status=status.HTTP_204_NO_CONTENT)  # ← No body, just success
        except StockItem.DoesNotExist:
            return Response({'error': 'Stock item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # ========================================
    # 📍 CUSTOM ENDPOINT: GET /api/stock/items/my_stock/
    # @action decorator creates custom route
    # Node.js: router.get('/items/my-stock', controller.getMyStock)
    # ========================================
    @action(detail=False, methods=['get'])
    def my_stock(self, request):
        """
        @action creates a CUSTOM endpoint
        detail=False means: /items/my_stock/ (no ID needed)
        detail=True would be: /items/:id/custom_action/
        
        This is same as list() but explicitly named
        """
        items = StockItem.objects(hunter_id=request.user.id)
        serializer = StockItemSerializer(items, many=True)
        return Response(serializer.data)
    
    # ========================================
    # 📍 CUSTOM ENDPOINT: POST /api/stock/items/:id/increase_quantity/
    # Node.js: router.post('/items/:id/increase-quantity', controller.increaseQty)
    # ========================================
    @action(detail=True, methods=['post'])
    def increase_quantity(self, request, pk=None):
        """
        detail=True means: needs an ID (/items/:id/increase_quantity/)
        
        Node.js equivalent:
        
        exports.increaseQuantity = async (req, res) => {
            const item = await StockItem.findOne({ _id: req.params.id, hunterId: req.user.id });
            if (!item) return res.status(404).json({ error: 'Not found' });
            
            const amount = parseInt(req.body.amount) || 1;
            item.quantity += amount;
            await item.save();
            
            res.json(item);
        }
        """
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            
            # BUSINESS LOGIC (this should be in service layer!)
            amount = int(request.data.get('amount', 1))
            item.quantity += amount
            item.save()
            
            serializer = StockItemSerializer(item)
            return Response(serializer.data)
        except StockItem.DoesNotExist:
            return Response({'error': 'Stock item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # ========================================
    # 📍 CUSTOM ENDPOINT: POST /api/stock/items/:id/decrease_quantity/
    # ========================================
    @action(detail=True, methods=['post'])
    def decrease_quantity(self, request, pk=None):
        """
        Same as increase_quantity but decreases
        Uses max(0, ...) to prevent negative quantities
        """
        try:
            item = StockItem.objects.get(id=pk, hunter_id=request.user.id)
            
            # BUSINESS LOGIC
            amount = int(request.data.get('amount', 1))
            item.quantity = max(0, item.quantity - amount)  # ← Never go below 0
            item.save()
            
            serializer = StockItemSerializer(item)
            return Response(serializer.data)
        except StockItem.DoesNotExist:
            return Response({'error': 'Stock item not found'}, status=status.HTTP_404_NOT_FOUND)
```

---

## 🎯 KEY TAKEAWAYS

### 1. ViewSet Methods = Express Route Handlers
```python
# Django ViewSet
def list(self, request):        → GET    /items/
def create(self, request):      → POST   /items/
def retrieve(self, request, pk):→ GET    /items/:id/
def update(self, request, pk):  → PUT    /items/:id/
def partial_update(self, pk):   → PATCH  /items/:id/
def destroy(self, request, pk): → DELETE /items/:id/

# Custom actions with @action decorator
@action(detail=False)           → GET/POST /items/custom_name/
@action(detail=True)            → GET/POST /items/:id/custom_name/
```

### 2. This File Does TOO MUCH!
In Node.js best practices, you'd split:
- **views.py** → controller (HTTP handling)
- **services/** → business logic (quantity manipulation)
- **repositories/** → database queries

Django combines them all in views.py by default!

### 3. Where's async/await?
Django REST Framework is synchronous by default.
Node.js: `async/await` everywhere
Django: Sync by default (async is optional)

---

## 📊 COMPARISON TABLE

| Django ViewSet | Node.js Express |
|----------------|-----------------|
| `list()` | `getAllItems()` |
| `create()` | `createItem()` |
| `retrieve()` | `getItemById()` |
| `update()` | `updateItem()` |
| `partial_update()` | `patchItem()` |
| `destroy()` | `deleteItem()` |
| `@action` | Custom route handler |
| `permission_classes` | Middleware |
| `serializer.is_valid()` | Joi validation |
| `Response()` | `res.json()` |
| `StockItem.objects` | `StockItem.find()` |

---

## 🤔 Want to see:
1. How serializers.py maps to Node.js validators?
2. How models.py maps to Mongoose schemas?
3. How to add a Service Layer (like Node.js)?
4. The complete request flow with diagrams?

Just ask! 🚀
