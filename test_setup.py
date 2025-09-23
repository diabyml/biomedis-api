#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_environment():
    """Test that environment variables are loaded correctly"""
    required_vars = ['SECRET_KEY', 'DATABASE_URL']
    
    print("🔧 Testing Environment Configuration...")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Missing")
            return False
    return True

def test_imports():
    """Test that all modules can be imported correctly"""
    print("\n📦 Testing Module Imports...")
    
    try:
        from app.routers import frontend, admin, auth
        from app import main, models, database
        print("✅ All modules import successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Project Setup...\n")
    
    env_ok = test_environment()
    imports_ok = test_imports()
    
    if env_ok and imports_ok:
        print("\n🎉 All tests passed! Project setup is correct.")
        print("\nNext steps:")
        print("1. Run: alembic upgrade head (to create database tables)")
        print("2. Run: uvicorn app.main:app --reload (to start server)")
        print("3. Visit: http://localhost:8000")
    else:
        print("\n💥 Some tests failed. Please check your setup.")
        sys.exit(1)