# 🚀 Quick Start Guide

## Prerequisites Check
```bash
# Check Python version (should be 3.14+)
python3 --version

# Check if MongoDB is running
brew services list | grep mongodb
```

## Start the Project (Every Time)

### 1. Activate Virtual Environment
```bash
cd /Users/mohamedmamdouh/Desktop/Web/Backend/Django
source venv/bin/activate
```

### 2. Start MongoDB (if not running)
```bash
brew services start mongodb/brew/mongodb-community
```

### 3. Start Django Server
```bash
python manage.py runserver
```

Server will be available at: **http://127.0.0.1:8000**

## First Time Setup Only

### Create Admin User
```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

## Testing the API

### Option 1: Use the Test Script
```bash
# In a new terminal (keep server running)
cd /Users/mohamedmamdouh/Desktop/Web/Backend/Django
source venv/bin/activate
pip install requests  # First time only
python test_api.py
```

### Option 2: Use Postman
1. Open Postman
2. Import `Hunter_Stock_API.postman_collection.json`
3. Start with "Authentication" → "Register"
4. Then "Authentication" → "Login" (saves tokens automatically)
5. Try other endpoints

### Option 3: Use cURL

**Register:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "hunter1",
    "email": "hunter1@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
  }'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "hunter1",
    "password": "SecurePass123!"
  }'
```

**Create Stock Item (replace YOUR_TOKEN):**
```bash
curl -X POST http://127.0.0.1:8000/api/stock/items/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dragon Sword",
    "quantity": 5,
    "item_type": "weapon"
  }'
```

**Get All Stock:**
```bash
curl -X GET http://127.0.0.1:8000/api/stock/items/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## API Endpoints Summary

### Authentication (No token needed)
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (get tokens)
- `POST /api/auth/token/refresh/` - Refresh access token

### Authentication (Token required)
- `GET /api/auth/profile/` - Get your profile
- `PATCH /api/auth/profile/` - Update profile
- `POST /api/auth/logout/` - Logout

### Stock Management (All require token)
- `GET /api/stock/items/` - List all your items
- `POST /api/stock/items/` - Create new item
- `GET /api/stock/items/{id}/` - Get specific item
- `PUT /api/stock/items/{id}/` - Update item (all fields)
- `PATCH /api/stock/items/{id}/` - Update item (partial)
- `DELETE /api/stock/items/{id}/` - Delete item
- `GET /api/stock/items/my_stock/` - Get your stock
- `POST /api/stock/items/{id}/increase_quantity/` - Increase quantity
- `POST /api/stock/items/{id}/decrease_quantity/` - Decrease quantity

## Common Issues & Solutions

### 1. MongoDB not running
**Error:** Connection refused
**Solution:**
```bash
brew services start mongodb/brew/mongodb-community
```

### 2. Port already in use
**Error:** Port 8000 is already in use
**Solution:**
```bash
# Find process using port 8000
lsof -ti:8000

# Kill the process
kill -9 $(lsof -ti:8000)

# Or use a different port
python manage.py runserver 8001
```

### 3. Virtual environment not activated
**Symptom:** Command not found or module errors
**Solution:**
```bash
source venv/bin/activate
```

### 4. Database migrations needed
**Error:** Migration errors
**Solution:**
```bash
python manage.py migrate
```

## Stop Everything

### Stop Django Server
Press `CTRL + C` in the terminal running the server

### Stop MongoDB (Optional)
```bash
brew services stop mongodb/brew/mongodb-community
```

### Deactivate Virtual Environment
```bash
deactivate
```

## Admin Panel

Access Django admin at: **http://127.0.0.1:8000/admin/**

Login with the superuser credentials you created.

**Note:** MongoDB stock items won't show in admin (MongoEngine limitation), but you can manage users there.

## Monitoring MongoDB

### Connect to MongoDB shell
```bash
mongosh
```

### View databases
```javascript
show dbs
```

### Use hunter stock database
```javascript
use hunter_stock_db
```

### View collections
```javascript
show collections
```

### Query stock items
```javascript
db.stock_items.find().pretty()
```

### Count items
```javascript
db.stock_items.count()
```

### Exit MongoDB shell
```javascript
exit
```

## Project Structure
```
Django/
├── apps/
│   ├── authentication/     # JWT auth, user management
│   └── stock/             # Stock CRUD operations
├── config/                # Django settings & URLs
├── venv/                  # Virtual environment
├── manage.py             # Django management
├── requirements.txt      # Python dependencies
├── README.md            # Full documentation
├── test_api.py          # Automated API tests
└── Hunter_Stock_API.postman_collection.json
```

## Learning Resources

- **Django Docs:** https://docs.djangoproject.com/
- **Django REST Framework:** https://www.django-rest-framework.org/
- **MongoEngine:** https://docs.mongoengine.org/
- **JWT:** https://jwt.io/

## Next Steps

1. ✅ Get the server running
2. ✅ Create a user account
3. ✅ Test all endpoints
4. 📚 Read the full README.md
5. 🎯 Start customizing for your needs

---

**Happy Coding! 🎉**
