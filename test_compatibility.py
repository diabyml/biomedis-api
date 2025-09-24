#!/usr/bin/env python3
import sys
import subprocess

def test_python_version():
    """Test Python version compatibility"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    # Recommend Python 3.11 for stability
    if version.major == 3 and version.minor >= 11:
        print("✅ Python version is compatible")
        return True
    else:
        print("⚠️  Consider using Python 3.11+ for better compatibility")
        return True  # Still allow older versions

def test_sqlalchemy_import():
    """Test SQLAlchemy import compatibility"""
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy version: {sqlalchemy.__version__}")
        # Test basic functionality
        from sqlalchemy.engine.create import create_engine
        from sqlalchemy.sql.expression import text
        engine = create_engine("sqlite:///:memory:")
        conn = engine.connect()
        try:
            result = conn.execute(text("SELECT 1"))
            print("✅ SQLAlchemy basic functionality works")
        finally:
            conn.close()
        return True
    except Exception as e:
        print(f"❌ SQLAlchemy import error: {e}")
        return False

def test_fastapi_import():
    """Test FastAPI import compatibility"""
    try:
        import fastapi
        import uvicorn
        print(f"✅ FastAPI version: {fastapi.__version__}")
        print(f"✅ Uvicorn version: {uvicorn.__version__}")
        return True
    except Exception as e:
        print(f"❌ FastAPI import error: {e}")
        return False

def test_application_import():
    """Test if the application can be imported"""
    try:
        from app.main import app
        from app.database import get_db, engine
        print("✅ Application modules import successfully")
        return True
    except Exception as e:
        print(f"❌ Application import error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing Compatibility...\n")
    
    tests = [
        test_python_version,
        test_sqlalchemy_import,
        test_fastapi_import,
        test_application_import,
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 All compatibility tests passed!")
        print("\nThe application should deploy successfully on Render.")
    else:
        print("💥 Some compatibility tests failed.")
        print("\nRecommended fixes:")
        print("1. Use Python 3.11 in runtime.txt")
        print("2. Ensure requirements versions are compatible")
        print("3. Check for circular imports")
        
    sys.exit(0 if all_passed else 1)