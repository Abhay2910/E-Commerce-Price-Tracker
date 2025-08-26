#!/usr/bin/env python3
"""
Pricely - Run Script
This script initializes and runs the Pricely application.
"""

import os
import sys
from app import app, db

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import requests
        import bs4
        import selenium
        import sqlalchemy
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("⚠️  No .env file found")
        print("Creating .env file from template...")
        
        env_content = """# Flask Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production

# Database Configuration
DATABASE_URL=sqlite:///price_tracker.db

# Email Configuration (Gmail Example)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true

# Scraping Configuration
SCRAPING_DELAY=5
DEFAULT_CHECK_INTERVAL=3600
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✓ Created .env file")
        print("⚠️  Please configure your email settings in .env file for notifications")
    else:
        print("✓ .env file found")

def initialize_database():
    """Initialize the database"""
    try:
        with app.app_context():
            db.create_all()
            print("✓ Database initialized")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False
    return True

def main():
    """Main function to run the application"""
    print("🚀 Starting Pricely...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment file
    check_env_file()
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    print("=" * 50)
    print("✅ Application ready!")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("📧 Configure email settings in .env file for notifications")
    print("=" * 50)
    
    # Run the application
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"✗ Application error: {e}")

if __name__ == '__main__':
    main()
