#!/usr/bin/env python
"""
API Testing Script
Run this after starting the server to test all endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def main():
    print("\n🚀 Testing Hunter Stock API")
    
    # 1. Register a new user
    print("\n1️⃣  Registering new user...")
    register_data = {
        "username": "hunter_test",
        "email": "hunter@test.com",
        "password": "TestPass123!",
        "password2": "TestPass123!",
        "first_name": "Test",
        "last_name": "Hunter"
    }
    response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
    print_response("Register User", response)
    
    # 2. Login
    print("\n2️⃣  Logging in...")
    login_data = {
        "username": "hunter_test",
        "password": "TestPass123!"
    }
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    print_response("Login", response)
    
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access']
        refresh_token = tokens['refresh']
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 3. Get Profile
        print("\n3️⃣  Getting user profile...")
        response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
        print_response("User Profile", response)
        
        # 4. Create stock items
        print("\n4️⃣  Creating stock items...")
        stock_items = [
            {"name": "Dragon Sword", "quantity": 5, "item_type": "weapon"},
            {"name": "Health Potion", "quantity": 20, "item_type": "consumable"},
            {"name": "Steel Armor", "quantity": 2, "item_type": "armor"}
        ]
        
        created_items = []
        for item in stock_items:
            response = requests.post(f"{BASE_URL}/stock/items/", json=item, headers=headers)
            print_response(f"Create: {item['name']}", response)
            if response.status_code == 201:
                created_items.append(response.json()['id'])
        
        # 5. List all stock items
        print("\n5️⃣  Listing all stock items...")
        response = requests.get(f"{BASE_URL}/stock/items/", headers=headers)
        print_response("All Stock Items", response)
        
        # 6. Get single item
        if created_items:
            print(f"\n6️⃣  Getting single item (ID: {created_items[0]})...")
            response = requests.get(f"{BASE_URL}/stock/items/{created_items[0]}/", headers=headers)
            print_response("Single Item", response)
            
            # 7. Increase quantity
            print(f"\n7️⃣  Increasing quantity...")
            response = requests.post(
                f"{BASE_URL}/stock/items/{created_items[0]}/increase_quantity/",
                json={"amount": 10},
                headers=headers
            )
            print_response("Increase Quantity", response)
            
            # 8. Decrease quantity
            print(f"\n8️⃣  Decreasing quantity...")
            response = requests.post(
                f"{BASE_URL}/stock/items/{created_items[0]}/decrease_quantity/",
                json={"amount": 3},
                headers=headers
            )
            print_response("Decrease Quantity", response)
            
            # 9. Update item
            print(f"\n9️⃣  Updating item...")
            update_data = {
                "name": "Dragon Sword +1",
                "quantity": 8,
                "item_type": "legendary_weapon"
            }
            response = requests.put(
                f"{BASE_URL}/stock/items/{created_items[0]}/",
                json=update_data,
                headers=headers
            )
            print_response("Update Item", response)
            
            # 10. Partial update
            print(f"\n🔟 Partial update...")
            response = requests.patch(
                f"{BASE_URL}/stock/items/{created_items[0]}/",
                json={"quantity": 100},
                headers=headers
            )
            print_response("Partial Update", response)
        
        # 11. My stock endpoint
        print("\n1️⃣1️⃣  Getting my stock...")
        response = requests.get(f"{BASE_URL}/stock/items/my_stock/", headers=headers)
        print_response("My Stock", response)
        
        # 12. Delete an item
        if len(created_items) > 1:
            print(f"\n1️⃣2️⃣  Deleting item (ID: {created_items[1]})...")
            response = requests.delete(
                f"{BASE_URL}/stock/items/{created_items[1]}/",
                headers=headers
            )
            print_response("Delete Item", response)
        
        # 13. Refresh token
        print("\n1️⃣3️⃣  Refreshing access token...")
        response = requests.post(
            f"{BASE_URL}/auth/token/refresh/",
            json={"refresh": refresh_token}
        )
        print_response("Refresh Token", response)
        
        # 14. Logout
        print("\n1️⃣4️⃣  Logging out...")
        response = requests.post(
            f"{BASE_URL}/auth/logout/",
            json={"refresh_token": refresh_token},
            headers=headers
        )
        print_response("Logout", response)
    
    print("\n" + "="*60)
    print("  ✅ API Testing Complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server!")
        print("Make sure the Django server is running: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Error: {e}")
