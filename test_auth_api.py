#!/usr/bin/env python3
"""
Test script for the Django Authentication API
Tests login, logout, and profile endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/auth"

def test_login():
    """Test login endpoint"""
    print("🔐 Testing Login API...")
    
    # Test with valid credentials
    login_data = {
        "username": "testuser1",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Login successful!")
        print(f"   Access Token: {data['access'][:50]}...")
        print(f"   Refresh Token: {data['refresh'][:50]}...")
        print(f"   User ID: {data['user']['id']}")
        print(f"   Username: {data['user']['username']}")
        return data['access']
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def test_profile(access_token):
    """Test profile endpoint with token"""
    if not access_token:
        print("⏭️  Skipping profile test (no access token)")
        return
    
    print("\n👤 Testing Profile API...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Profile fetch successful!")
        print(f"   User ID: {data['id']}")
        print(f"   Username: {data['username']}")
        print(f"   Email: {data['email']}")
        print(f"   First Name: {data['first_name']}")
        print(f"   Last Name: {data['last_name']}")
        print(f"   Date Joined: {data['date_joined']}")
    else:
        print(f"❌ Profile fetch failed: {response.status_code}")
        print(f"   Response: {response.text}")

def test_logout(access_token):
    """Test logout endpoint"""
    if not access_token:
        print("⏭️  Skipping logout test (no access token)")
        return
    
    print("\n🚪 Testing Logout API...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{BASE_URL}/logout/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Logout successful!")
        print(f"   Message: {data['message']}")
    else:
        print(f"❌ Logout failed: {response.status_code}")
        print(f"   Response: {response.text}")

def test_invalid_login():
    """Test login with invalid credentials"""
    print("\n🔒 Testing Invalid Login...")
    
    login_data = {
        "username": "invaliduser",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=login_data)
    
    if response.status_code == 400:
        data = response.json()
        print("✅ Invalid login correctly rejected!")
        print(f"   Error: {data['error']}")
    else:
        print(f"❌ Expected 400 status but got: {response.status_code}")
        print(f"   Response: {response.text}")

def main():
    """Run all tests"""
    print("🚀 Starting Authentication API Tests")
    print("=" * 50)
    
    # Test valid login
    access_token = test_login()
    
    # Test profile with valid token
    test_profile(access_token)
    
    # Test logout
    test_logout(access_token)
    
    # Test invalid login
    test_invalid_login()
    
    print("\n" + "=" * 50)
    print("🏁 All tests completed!")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Django server.")
        print("   Make sure the server is running on http://127.0.0.1:8000/")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
