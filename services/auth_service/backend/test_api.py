#!/usr/bin/env python
"""
Simple API test script for Django Authentication Service.

This script demonstrates how to interact with the authentication API
and can be used for basic testing and validation.
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_USERNAME = "testuser1"  # Changed from email to username
TEST_PASSWORD = "testpass123"

class AuthAPITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
        self.session = requests.Session()
    
    def test_login(self, username, password):
        """Test the login endpoint with username and password."""
        print(f"\n🔐 Testing login with username: {username}...")
        
        url = f"{self.base_url}/api/v1/auth/login/"
        data = {
            "username": username,
            "password": password
        }
        
        try:
            response = self.session.post(url, json=data)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("✅ Login successful!")
                    
                    # Store tokens
                    tokens = result['data']['tokens']
                    self.access_token = tokens['access']
                    self.refresh_token = tokens['refresh']
                    
                    # Display user info
                    user = result['data']['user']
                    print(f"   User ID: {user['id']}")
                    print(f"   Username: {user['username']}")
                    print(f"   Email: {user['email']}")
                    print(f"   Name: {user['first_name']} {user['last_name']}")
                    
                    return True
                else:
                    print(f"❌ Login failed: {result.get('message')}")
                    print(f"   Errors: {result.get('errors')}")
            else:
                print(f"❌ HTTP Error {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                    
        except requests.RequestException as e:
            print(f"❌ Request failed: {e}")
            
        return False
    
    def test_profile(self):
        """Test the profile endpoint."""
        if not self.access_token:
            print("❌ No access token available. Please login first.")
            return False
        
        print(f"\n👤 Testing profile endpoint...")
        
        url = f"{self.base_url}/api/v1/auth/profile/"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = self.session.get(url, headers=headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("✅ Profile retrieved successfully!")
                    user = result['data']['user']
                    print(f"   Profile data: {json.dumps(user, indent=2)}")
                    return True
                else:
                    print(f"❌ Profile request failed: {result.get('message')}")
            else:
                print(f"❌ HTTP Error {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                    
        except requests.RequestException as e:
            print(f"❌ Request failed: {e}")
            
        return False
    
    def test_token_refresh(self):
        """Test the token refresh endpoint."""
        if not self.refresh_token:
            print("❌ No refresh token available. Please login first.")
            return False
        
        print(f"\n🔄 Testing token refresh...")
        
        url = f"{self.base_url}/api/v1/auth/token/refresh/"
        data = {
            "refresh": self.refresh_token
        }
        
        try:
            response = self.session.post(url, json=data)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if 'access' in result:
                    print("✅ Token refresh successful!")
                    old_token = self.access_token[:20] + "..."
                    self.access_token = result['access']
                    new_token = self.access_token[:20] + "..."
                    print(f"   Old token: {old_token}")
                    print(f"   New token: {new_token}")
                    return True
                else:
                    print(f"❌ Token refresh failed: {result}")
            else:
                print(f"❌ HTTP Error {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                    
        except requests.RequestException as e:
            print(f"❌ Request failed: {e}")
            
        return False
    
    def test_logout(self):
        """Test the logout endpoint."""
        if not self.refresh_token:
            print("❌ No refresh token available. Please login first.")
            return False
        
        print(f"\n🚪 Testing logout...")
        
        url = f"{self.base_url}/api/v1/auth/logout/"
        headers = {}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        data = {
            "refresh": self.refresh_token
        }
        
        try:
            response = self.session.post(url, json=data, headers=headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("✅ Logout successful!")
                    print(f"   Message: {result.get('message')}")
                    
                    # Clear tokens
                    self.access_token = None
                    self.refresh_token = None
                    return True
                else:
                    print(f"❌ Logout failed: {result.get('message')}")
            else:
                print(f"❌ HTTP Error {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                    
        except requests.RequestException as e:
            print(f"❌ Request failed: {e}")
            
        return False
    
    def test_invalid_credentials(self):
        """Test login with invalid credentials."""
        print(f"\n🚫 Testing login with invalid credentials...")
        
        url = f"{self.base_url}/api/v1/auth/login/"
        data = {
            "username": "invalid_user",
            "password": "wrongpassword"
        }
        
        try:
            response = self.session.post(url, json=data)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 400:
                result = response.json()
                if not result.get('success'):
                    print("✅ Invalid credentials correctly rejected!")
                    print(f"   Message: {result.get('message')}")
                    return True
                else:
                    print("❌ Invalid credentials were accepted (unexpected)")
            else:
                print(f"❌ Unexpected status code: {response.status_code}")
                
        except requests.RequestException as e:
            print(f"❌ Request failed: {e}")
            
        return False

def check_server_status(base_url):
    """Check if the Django server is running."""
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5)
        return response.status_code in [200, 302]  # 302 is redirect to login
    except requests.RequestException:
        return False

def main():
    """Main test function."""
    print("🧪 Django Authentication API Tester")
    print("=" * 50)
    
    # Check if server is running
    print(f"🔍 Checking server status at {BASE_URL}...")
    if not check_server_status(BASE_URL):
        print("❌ Server is not running or not accessible.")
        print("   Please make sure the Django development server is running:")
        print("   python manage.py runserver")
        sys.exit(1)
    
    print("✅ Server is running!")
    
    # Initialize tester
    tester = AuthAPITester(BASE_URL)
    
    # Run tests
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Valid login
    total_tests += 1
    if tester.test_login(TEST_USERNAME, TEST_PASSWORD):
        tests_passed += 1
    
    # Test 2: Profile endpoint
    total_tests += 1
    if tester.test_profile():
        tests_passed += 1
    
    # Test 3: Token refresh
    total_tests += 1
    if tester.test_token_refresh():
        tests_passed += 1
    
    # Test 4: Logout
    total_tests += 1
    if tester.test_logout():
        tests_passed += 1
    
    # Test 5: Invalid credentials
    total_tests += 1
    if tester.test_invalid_credentials():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Test Summary")
    print("=" * 30)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    print(f"Success rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the server logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
