# 🛠️ Useful Django Management Commands

## Basic Commands

### Run Development Server
```bash
python manage.py runserver
# Or on different port
python manage.py runserver 8001
```

### Check for Issues
```bash
python manage.py check
```

### Django Shell (Interactive Python)
```bash
python manage.py shell
```

---

## User Management

### Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Change User Password
```bash
python manage.py changepassword username
```

---

## Database Commands

### Make Migrations (Create migration files)
```bash
python manage.py makemigrations
```

### Run Migrations (Apply to database)
```bash
python manage.py migrate
```

### Show Migrations
```bash
python manage.py showmigrations
```

### SQL for Migration
```bash
python manage.py sqlmigrate app_name migration_name
```

---

## MongoDB Queries (in Django Shell)

### Open Shell
```bash
python manage.py shell
```

### Query Stock Items
```python
from apps.stock.models import StockItem
from django.contrib.auth.models import User

# Get all items
items = StockItem.objects.all()
for item in items:
    print(f"{item.name}: {item.quantity}")

# Get items for specific user
user = User.objects.get(username='hunter1')
my_items = StockItem.objects(hunter_id=user.id)

# Create new item
new_item = StockItem(
    name="Test Item",
    quantity=10,
    item_type="test",
    hunter_id=1
)
new_item.save()

# Update item
item = StockItem.objects.first()
item.quantity = 100
item.save()

# Delete item
item.delete()

# Count items
count = StockItem.objects.count()
print(f"Total items: {count}")
```

### Query Users
```python
from django.contrib.auth.models import User

# Get all users
users = User.objects.all()

# Get specific user
user = User.objects.get(username='hunter1')

# Create user
user = User.objects.create_user(
    username='newuser',
    email='new@example.com',
    password='password123'
)
```

---

## Testing

### Run All Tests
```bash
python manage.py test
```

### Run Specific App Tests
```bash
python manage.py test apps.stock
```

### Run with Verbosity
```bash
python manage.py test --verbosity=2
```

---

## Static Files

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

---

## Database Inspection

### Show Database
```bash
python manage.py dbshell
```

---

## Custom Management (for future)

### Create Custom Command
1. Create: `apps/stock/management/commands/my_command.py`
2. Run: `python manage.py my_command`

Example structure:
```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Description of command'
    
    def handle(self, *args, **options):
        self.stdout.write('Executing command...')
```

---

## Development Workflow

### 1. Start New Feature
```bash
# Activate environment
source venv/bin/activate

# Start MongoDB
brew services start mongodb/brew/mongodb-community

# Run server
python manage.py runserver
```

### 2. Make Changes
- Edit models, views, serializers
- Test in browser or Postman

### 3. If Model Changed
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Test
```bash
python test_api.py
# Or use Postman
```

---

## Troubleshooting Commands

### Reset Database (SQLite only - careful!)
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Clear MongoDB Collections
```bash
# In mongo shell
mongosh
use hunter_stock_db
db.stock_items.deleteMany({})
```

### View Logs
```bash
# Server logs appear in terminal
# Or check specific log file if configured
```

### Check Python Packages
```bash
pip list
pip show package_name
```

### Update Package
```bash
pip install --upgrade package_name
```

---

## Production Checklist

### Before Deployment
```bash
# Check for issues
python manage.py check --deploy

# Collect static files
python manage.py collectstatic

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Update Settings
- Set `DEBUG = False`
- Add allowed hosts
- Use production database
- Set secure secret key
- Configure static/media files

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `runserver` | Start dev server |
| `migrate` | Apply database changes |
| `makemigrations` | Create migration files |
| `createsuperuser` | Create admin user |
| `shell` | Python interactive shell |
| `test` | Run tests |
| `check` | Check for issues |
| `collectstatic` | Gather static files |

---

## Virtual Environment Commands

### Activate
```bash
source venv/bin/activate
```

### Deactivate
```bash
deactivate
```

### Install Package
```bash
pip install package_name
```

### Save Dependencies
```bash
pip freeze > requirements.txt
```

### Install from requirements
```bash
pip install -r requirements.txt
```

---

## MongoDB Service Commands

### Start
```bash
brew services start mongodb/brew/mongodb-community
```

### Stop
```bash
brew services stop mongodb/brew/mongodb-community
```

### Restart
```bash
brew services restart mongodb/brew/mongodb-community
```

### Status
```bash
brew services list
```

### Connect to Shell
```bash
mongosh
```

---

**Keep this file handy for quick reference! 📖**
