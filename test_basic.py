#!/usr/bin/env python
"""
Basic test script to verify Django setup
Run this locally to test if Django is configured correctly
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'claims_interface.settings')

# Setup Django
django.setup()

from django.conf import settings
from django.db import connection

def test_django_setup():
    """Test basic Django setup"""
    print("Testing Django setup...")
    
    # Test settings
    print(f"DEBUG: {settings.DEBUG}")
    print(f"SECRET_KEY set: {bool(settings.SECRET_KEY)}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"Database engine: {settings.DATABASES['default']['ENGINE']}")
    
    # Test database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("Database connection: OK")
    except Exception as e:
        print(f"Database connection failed: {e}")
    
    # Test static files
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    
    print("Django setup test completed!")

if __name__ == "__main__":
    test_django_setup()
