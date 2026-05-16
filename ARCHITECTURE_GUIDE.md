# 🗺️ Django to Node.js Architecture Map

## Your Hunter Stock API Structure

```
apps/stock/
├── models.py        → 🟢 Mongoose Model (Data Layer)
├── serializers.py   → 🟡 DTO / Validator (Data Transfer)
├── views.py         → 🔵 Controller (Business Logic)
├── urls.py          → 🟣 Express Router (Routes)
└── [NO SERVICE LAYER] → ❌ Missing (we can add!)
```

---

## 🎯 Layer-by-Layer Comparison

### 📍 1. ENDPOINT LAYER (Routing)

#### Django: `urls.py`
```python
# apps/stock/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockItemViewSet

router = DefaultRouter()
router.register(r'items', StockItemViewSet, basename='stock-item')

urlpatterns = [
    path('', include(router.urls)),
]
```

#### Node.js Equivalent: `routes/stock.routes.js`
```javascript
// routes/stock.routes.js
const express = require('express');
const router = express.Router();
const stockController = require('../controllers/stock.controller');
const authMiddleware = require('../middleware/auth');

router.get('/items', authMiddleware, stockController.getAllItems);
router.post('/items', authMiddleware, stockController.createItem);
router.get('/items/:id', authMiddleware, stockController.getItem);
router.put('/items/:id', authMiddleware, stockController.updateItem);
router.delete('/items/:id', authMiddleware, stockController.deleteItem);

module.exports = router;
```

**Key Difference:**
- Django: Uses `DefaultRouter` (auto-generates REST routes)
- Node.js: Manual route definition

---

### 🎮 2. CONTROLLER LAYER (Request Handling)

#### Django: `views.py`
```python
# apps/stock/views.py
from rest_framework import viewsets, permissions

class StockItemViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        # Get all items
        items = StockItem.objects(hunter_id=request.user.id)
        serializer = StockItemSerializer(items, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        # Create new item
        serializer = StockItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

#### Node.js Equivalent: `controllers/stock.controller.js`
```javascript
// controllers/stock.controller.js
const StockItem = require('../models/StockItem');

exports.getAllItems = async (req, res) => {
    try {
        const items = await StockItem.find({ hunterId: req.user.id });
        res.json(items);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

exports.createItem = async (req, res) => {
    try {
        const item = new StockItem({
            ...req.body,
            hunterId: req.user.id
        });
        await item.save();
        res.status(201).json(item);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
};
```

**Key Difference:**
- Django: Uses `ViewSet` classes (bundles CRUD methods)
- Node.js: Individual controller functions

---

### 🔄 3. SERIALIZER/VALIDATOR LAYER (Data Transfer)

#### Django: `serializers.py`
```python
# apps/stock/serializers.py
from rest_framework import serializers

class StockItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200, required=True)
    quantity = serializers.IntegerField(default=0)
    item_type = serializers.CharField(max_length=100, required=True)
    
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative")
        return value
    
    def create(self, validated_data):
        validated_data['hunter_id'] = self.context['request'].user.id
        stock_item = StockItem(**validated_data)
        stock_item.save()
        return stock_item
```

#### Node.js Equivalent: `validators/stock.validator.js` + DTO
```javascript
// validators/stock.validator.js
const Joi = require('joi');

const createStockSchema = Joi.object({
    name: Joi.string().max(200).required(),
    quantity: Joi.number().integer().min(0).default(0),
    item_type: Joi.string().max(100).required()
});

exports.validateCreateStock = (req, res, next) => {
    const { error, value } = createStockSchema.validate(req.body);
    if (error) {
        return res.status(400).json({ error: error.details[0].message });
    }
    req.validatedData = value;
    next();
};

// dto/stock.dto.js
class StockItemDTO {
    constructor(stockItem) {
        this.id = stockItem._id;
        this.name = stockItem.name;
        this.quantity = stockItem.quantity;
        this.item_type = stockItem.item_type;
        this.hunter_username = stockItem.hunter?.username;
        this.created_at = stockItem.created_at;
        this.updated_at = stockItem.updated_at;
    }
}
```

**Key Difference:**
- Django: Serializers handle BOTH validation AND transformation
- Node.js: Typically split between validators (Joi/Yup) and DTOs

---

### 💾 4. MODEL LAYER (Data/Database)

#### Django: `models.py`
```python
# apps/stock/models.py
from mongoengine import Document, StringField, IntField, DateTimeField
import datetime

class StockItem(Document):
    name = StringField(required=True, max_length=200)
    quantity = IntField(default=0)
    item_type = StringField(required=True, max_length=100)
    hunter_id = IntField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    
    meta = {
        'collection': 'stock_items',
        'ordering': ['-created_at']
    }
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(StockItem, self).save(*args, **kwargs)
```

#### Node.js Equivalent: `models/StockItem.js`
```javascript
// models/StockItem.js (Mongoose)
const mongoose = require('mongoose');

const stockItemSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
        maxlength: 200
    },
    quantity: {
        type: Number,
        default: 0
    },
    item_type: {
        type: String,
        required: true,
        maxlength: 100
    },
    hunterId: {
        type: Number,
        required: true
    }
}, {
    timestamps: true,  // auto creates createdAt, updatedAt
    collection: 'stock_items'
});

// Virtual for hunter
stockItemSchema.virtual('hunter', {
    ref: 'User',
    localField: 'hunterId',
    foreignField: '_id',
    justOne: true
});

module.exports = mongoose.model('StockItem', stockItemSchema);
```

**Key Difference:**
- Django: MongoEngine (similar to Mongoose)
- Node.js: Mongoose (almost identical!)

---

### 🔧 5. SERVICE LAYER (Business Logic)

#### Django: ❌ **DOESN'T EXIST BY DEFAULT!**

Your current structure puts business logic in `views.py` (controllers).

#### Node.js: `services/stock.service.js`
```javascript
// services/stock.service.js
const StockItem = require('../models/StockItem');

class StockService {
    async getItemsByHunter(hunterId) {
        return await StockItem.find({ hunterId });
    }
    
    async createItem(data, hunterId) {
        const item = new StockItem({ ...data, hunterId });
        return await item.save();
    }
    
    async increaseQuantity(itemId, hunterId, amount) {
        const item = await StockItem.findOne({ _id: itemId, hunterId });
        if (!item) throw new Error('Item not found');
        
        item.quantity += amount;
        return await item.save();
    }
    
    async calculateTotalValue(hunterId) {
        // Complex business logic here
        const items = await this.getItemsByHunter(hunterId);
        return items.reduce((total, item) => {
            return total + (item.quantity * item.value);
        }, 0);
    }
}

module.exports = new StockService();
```

**We can add this to Django!**

---

### 🔐 6. MIDDLEWARE LAYER

#### Django: Built-in + Custom
```python
# config/settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ← JWT Auth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # ← JWT
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # ← Auth required
    ),
}
```

#### Node.js Equivalent:
```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

module.exports = (req, res, next) => {
    try {
        const token = req.header('Authorization').replace('Bearer ', '');
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        next();
    } catch (error) {
        res.status(401).json({ error: 'Please authenticate' });
    }
};

// app.js
app.use(express.json());  // Body parser
app.use(cors());          // CORS
app.use(helmet());        // Security
```

---

## 🗺️ COMPLETE SIDE-BY-SIDE COMPARISON

### Node.js Express Structure
```
project/
├── routes/
│   ├── stock.routes.js       → Route definitions
│   └── auth.routes.js
├── controllers/
│   ├── stock.controller.js   → Request handlers
│   └── auth.controller.js
├── services/
│   ├── stock.service.js      → Business logic
│   └── auth.service.js
├── models/
│   ├── StockItem.js          → Database schema
│   └── User.js
├── middleware/
│   ├── auth.js               → Authentication
│   └── validation.js
├── validators/
│   └── stock.validator.js    → Input validation
├── dto/
│   └── stock.dto.js          → Data transformation
├── config/
│   └── database.js           → DB connection
└── app.js                    → Main entry
```

### Django REST Framework Structure (Your App)
```
apps/stock/
├── urls.py              → routes/ (Route definitions)
├── views.py             → controllers/ + services/ (!)
├── serializers.py       → validators/ + dto/
├── models.py            → models/
├── admin.py             → Admin panel registration
└── tests.py             → Test files

config/
├── settings.py          → config/ + middleware/
├── urls.py              → Main router
└── wsgi.py              → Server entry
```

---

## 🎯 KEY DIFFERENCES

| Feature | Node.js | Django |
|---------|---------|--------|
| **Routing** | Manual | Auto-generated (ViewSets) |
| **Controller** | Separate functions | Class methods |
| **Service Layer** | ✅ Explicit | ❌ Mixed in views |
| **Validation** | Joi/Yup middleware | Serializers |
| **DTO** | Manual classes | Serializers |
| **ORM** | Mongoose | MongoEngine (almost same!) |
| **Async** | async/await | sync by default |
| **Middleware** | Function chain | Settings list |

---

## 📊 REQUEST FLOW COMPARISON

### Node.js Express:
```
Request → 
  app.js → 
    routes/stock.routes.js → 
      middleware/auth.js → 
        validators/stock.validator.js → 
          controllers/stock.controller.js → 
            services/stock.service.js → 
              models/StockItem.js → 
                Database
```

### Django REST Framework:
```
Request → 
  config/urls.py → 
    apps/stock/urls.py → 
      REST_FRAMEWORK middleware (auth) → 
        views.py (ViewSet) → 
          serializers.py (validation) → 
            models.py (MongoEngine) → 
              Database
```

---

## 🤔 Want Me To:

1. **Show you the actual code** from your app with annotations?
2. **Add a Service Layer** to your Django app (like Node.js)?
3. **Create a comparison table** for specific features?
4. **Refactor your app** to be more Node.js-like with explicit layers?

**What would help you understand better?** 🎯
