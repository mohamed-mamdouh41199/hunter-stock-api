# Hunter Stock Management API

A modern Django REST API for managing hunter stock inventory using MongoDB and JWT authentication.

## 🏗️ Project Structure

```
Django/
├── apps/
│   ├── authentication/      # User authentication & JWT
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   └── stock/              # Stock management
│       ├── models.py       # MongoEngine models
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
├── config/                 # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── venv/                   # Virtual environment
├── .env                    # Environment variables
├── manage.py
└── requirements.txt
```

## 🚀 Technologies Used

### Backend Framework
- **Django 6.0.5** - Modern Python web framework
- **Django REST Framework 3.17.1** - Powerful REST API toolkit

### Database
- **MongoDB** - NoSQL database for stock data
- **MongoEngine 0.29.3** - MongoDB ODM (Object-Document Mapper)
- **SQLite** - Default Django database for user authentication
- **PyMongo 4.17.0** - MongoDB Python driver

### Authentication
- **djangorestframework-simplejwt 5.5.1** - JWT token authentication
- **PyJWT 2.12.1** - JSON Web Token implementation

### Additional Packages
- **python-dotenv 1.2.2** - Environment variable management
- **pytz 2026.2** - Timezone calculations
- **dnspython 2.8.0** - DNS toolkit for MongoDB connections

## 📦 Why These Packages Were Installed

1. **Django** - The main web framework providing the structure
2. **Django REST Framework** - Converts Django to a RESTful API platform
3. **MongoEngine** - Provides an elegant way to work with MongoDB using Python classes
4. **PyMongo** - Low-level MongoDB driver required by MongoEngine
5. **djangorestframework-simplejwt** - Implements JWT authentication for secure API access
6. **MongoDB (via Homebrew)** - The NoSQL database server
7. **python-dotenv** - Manages environment variables securely
8. **pytz** - Required dependency for Django timezone support
9. **dnspython** - Required for MongoDB connection string parsing

## 🔧 Setup Instructions

### 1. Prerequisites
- Python 3.14+
- MongoDB (installed via Homebrew)

### 2. Virtual Environment
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Edit `.env` file with your settings:
```env
SECRET_KEY=your-secret-key
DEBUG=True
MONGODB_URI=mongodb://localhost:27017/
MONGODB_NAME=hunter_stock_db
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Start MongoDB
```bash
brew services start mongodb/brew/mongodb-community
```

### 8. Run Development Server
```bash
python manage.py runserver
```

## 📡 API Endpoints

### Authentication Endpoints

#### Register New User
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "hunter1",
    "email": "hunter1@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Login (Get JWT Tokens)
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "hunter1",
    "password": "SecurePass123!"
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "your-refresh-token"
}
```

#### Logout
```http
POST /api/auth/logout/
Authorization: Bearer <access-token>
Content-Type: application/json

{
    "refresh_token": "your-refresh-token"
}
```

#### Get/Update Profile
```http
GET /api/auth/profile/
Authorization: Bearer <access-token>

PATCH /api/auth/profile/
Authorization: Bearer <access-token>
Content-Type: application/json

{
    "first_name": "Updated Name"
}
```

### Stock Management Endpoints

All stock endpoints require authentication via JWT token in the header:
```
Authorization: Bearer <your-access-token>
```

#### List All Stock Items
```http
GET /api/stock/items/
Authorization: Bearer <access-token>
```

#### Create Stock Item
```http
POST /api/stock/items/
Authorization: Bearer <access-token>
Content-Type: application/json

{
    "name": "Dragon Sword",
    "quantity": 5,
    "item_type": "weapon"
}
```

#### Get Single Stock Item
```http
GET /api/stock/items/{id}/
Authorization: Bearer <access-token>
```

#### Update Stock Item
```http
PUT /api/stock/items/{id}/
Authorization: Bearer <access-token>
Content-Type: application/json

{
    "name": "Dragon Sword +1",
    "quantity": 3,
    "item_type": "weapon"
}
```

#### Partial Update
```http
PATCH /api/stock/items/{id}/
Authorization: Bearer <access-token>
Content-Type: application/json

{
    "quantity": 10
}
```

#### Delete Stock Item
```http
DELETE /api/stock/items/{id}/
Authorization: Bearer <access-token>
```

#### Get My Stock (Custom Endpoint)
```http
GET /api/stock/items/my_stock/
Authorization: Bearer <access-token>
```

#### Increase Quantity
```http
POST /api/stock/items/{id}/increase_quantity/
Authorization: Bearer <access-token>
Content-Type: application/json

{
    "amount": 5
}
```

#### Decrease Quantity
```http
POST /api/stock/items/{id}/decrease_quantity/
Authorization: Bearer <access-token>
Content-Type: application/json

{
    "amount": 2
}
```

## 🔐 Authentication Flow

1. **Register** - Create a new user account
2. **Login** - Receive access token (1 hour) and refresh token (7 days)
3. **Use Access Token** - Include in Authorization header for all API requests
4. **Refresh Token** - Get new access token when it expires
5. **Logout** - Blacklist refresh token

## 🎯 Key Features

- ✅ JWT-based authentication with token refresh and blacklisting
- ✅ MongoDB integration for flexible stock data storage
- ✅ User isolation (users can only see their own stock)
- ✅ RESTful API design with proper HTTP methods
- ✅ Custom actions for quantity management
- ✅ Modern Django project structure with apps folder
- ✅ Environment-based configuration
- ✅ Automatic timestamp tracking

## 📚 Learning Points

### Modern Django Structure
- Organized apps in a dedicated `apps/` folder
- Separation of concerns (authentication vs business logic)
- Environment-based configuration using `.env`

### Database Architecture
- Hybrid approach: SQLite for auth, MongoDB for application data
- MongoEngine Document models vs Django ORM models
- Understanding when to use SQL vs NoSQL

### REST API Best Practices
- ViewSets for CRUD operations
- Serializers for data validation
- Permission classes for security
- Custom actions with `@action` decorator

### Authentication & Security
- JWT tokens for stateless authentication
- Token refresh mechanism
- Token blacklisting on logout
- User-specific data filtering

## 🛠️ Development Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run server
python manage.py runserver

# Create migrations (for Django models only)
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Check MongoDB status
brew services list | grep mongodb
```

## 📝 Notes

- Stock items are stored in MongoDB (flexible schema)
- User authentication is stored in SQLite (Django's default)
- JWT tokens expire: Access (1 hour), Refresh (7 days)
- All stock endpoints require authentication
- Users can only access their own stock items

## 🚨 Security Reminders

- Never commit `.env` file to git
- Change SECRET_KEY in production
- Set DEBUG=False in production
- Use strong passwords
- Keep dependencies updated

## 📖 Next Steps for Learning

1. Add filtering and search to stock items
2. Implement pagination
3. Add unit tests
4. Create API documentation with Swagger
5. Add image uploads for stock items
6. Implement stock categories
7. Add stock alerts for low quantities
8. Create analytics endpoints

---

Built with ❤️ for learning Django REST API & MongoDB
