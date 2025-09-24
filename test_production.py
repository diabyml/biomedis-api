#!/usr/bin/env python3
import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv('.env.production')

def test_production_readiness():
    """Test if the application is ready for production"""
    print("🔧 Testing Production Readiness...")
    
    # Test 1: Check critical environment variables
    critical_vars = ['SECRET_KEY', 'DATABASE_URL']
    missing_vars = []
    
    for var in critical_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ All environment variables are set")
    
    # Test 2: Check if we can import all modules
    try:
        from app import main, database, models
        from app.routers import frontend, admin, auth
        print("✅ All modules import successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 3: Check database connection
    try:
        from app.database import test_database_connection
        if test_database_connection():
            print("✅ Database connection successful")
        else:
            print("❌ Database connection failed")
            return False
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False
    
    # Test 4: Check if requirements are installed
    try:
        import fastapi, uvicorn, sqlalchemy, alembic, cloudinary, jwt, passlib
        print("✅ All required packages are installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        return False
    
    return True

def test_build_process():
    """Test the build process"""
    print("\n🏗️ Testing Build Process...")
    
    try:
        # Simulate build process
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Requirements installation successful")
        else:
            print(f"❌ Requirements installation failed: {result.stderr}")
            return False
            
        # Test migrations
        result = subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Database migrations successful")
        else:
            print(f"❌ Database migrations failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Build process test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Testing Production Deployment Readiness...\n")
    
    readiness_ok = test_production_readiness()
    build_ok = test_build_process()
    
    if readiness_ok and build_ok:
        print("\n🎉 Production readiness tests passed!")
        print("\n✅ You're ready to deploy to Render!")
        print("\nNext steps:")
        print("1. Push your code to GitHub")
        print("2. Connect your repository to Render")
        print("3. Set up environment variables in Render dashboard")
        print("4. Deploy!")
    else:
        print("\n💥 Some tests failed. Please fix issues before deploying.")
        sys.exit(1)