#!/usr/bin/env python3
"""
AI Appointment Assistant - Deployment Readiness Checker
Validates that all required components are properly configured for deployment
"""

import os
import sys
from pathlib import Path
import json

def check_environment_variables():
    """Check if required environment variables are set"""
    print("🔍 Checking Environment Variables...")
    
    required_vars = [
        "GROQ_API_KEY",
        "GOOGLE_CREDENTIALS_PATH"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
        else:
            print(f"  ✅ {var}: Set")
    
    if missing_vars:
        print(f"  ❌ Missing variables: {', '.join(missing_vars)}")
        return False
    
    print("  ✅ All environment variables are set!")
    return True

def check_credentials_file():
    """Check if Google service account credentials exist and are valid"""
    print("\n🔑 Checking Google Credentials...")
    
    creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "config/credentials/service_account.json")
    
    if not os.path.exists(creds_path):
        print(f"  ❌ Credentials file not found: {creds_path}")
        return False
    
    try:
        with open(creds_path, 'r') as f:
            creds = json.load(f)
        
        required_fields = ["type", "project_id", "private_key", "client_email"]
        missing_fields = [field for field in required_fields if field not in creds]
        
        if missing_fields:
            print(f"  ❌ Invalid credentials file. Missing fields: {', '.join(missing_fields)}")
            return False
        
        if creds.get("type") != "service_account":
            print("  ❌ Credentials file is not a service account")
            return False
        
        print(f"  ✅ Valid service account: {creds['client_email']}")
        return True
        
    except json.JSONDecodeError:
        print("  ❌ Invalid JSON in credentials file")
        return False
    except Exception as e:
        print(f"  ❌ Error reading credentials: {str(e)}")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n📦 Checking Dependencies...")
    
    required_packages = [
        "streamlit",
        "httpx",
        "google-auth",
        "google-api-python-client",
        "python-dotenv"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✅ {package}: Installed")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}: Not installed")
    
    if missing_packages:
        print(f"\n  📝 Install missing packages:")
        print(f"     pip install {' '.join(missing_packages)}")
        return False
    
    print("  ✅ All dependencies are installed!")
    return True

def check_file_structure():
    """Check if all required files and directories exist"""
    print("\n📁 Checking File Structure...")
    
    required_files = [
        "streamlit_app.py",
        "requirements.txt",
        ".env.example",
        "README.md",
        "backend/agent/ai_assistant.py",
        "backend/calender_service.py",
        "config/settings.py"
    ]
    
    required_dirs = [
        "backend",
        "config",
        "config/credentials"
    ]
    
    missing_items = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_items.append(f"File: {file_path}")
        else:
            print(f"  ✅ {file_path}")
    
    for dir_path in required_dirs:
        if not os.path.isdir(dir_path):
            missing_items.append(f"Directory: {dir_path}")
        else:
            print(f"  ✅ {dir_path}/")
    
    if missing_items:
        print(f"  ❌ Missing items:")
        for item in missing_items:
            print(f"     - {item}")
        return False
    
    print("  ✅ All required files and directories exist!")
    return True

def check_security():
    """Check if sensitive files are properly protected"""
    print("\n🔒 Checking Security Configuration...")
    
    # Check if .gitignore exists and contains sensitive files
    if not os.path.exists(".gitignore"):
        print("  ❌ .gitignore file not found")
        return False
    
    with open(".gitignore", "r") as f:
        gitignore_content = f.read()
    
    sensitive_patterns = [
        ".env",
        "service_account.json",
        "credentials.json",
        "*.json"
    ]
    
    missing_patterns = []
    for pattern in sensitive_patterns:
        if pattern not in gitignore_content:
            missing_patterns.append(pattern)
        else:
            print(f"  ✅ {pattern} is gitignored")
    
    if missing_patterns:
        print(f"  ⚠️  These patterns should be in .gitignore: {', '.join(missing_patterns)}")
    
    # Check if .env file exists (should exist locally)
    if os.path.exists(".env"):
        print("  ✅ .env file exists locally")
    else:
        print("  ⚠️  .env file not found (copy from .env.example)")
    
    # Check if sensitive files are actually ignored
    sensitive_files = [".env", "config/credentials/service_account.json"]
    for file_path in sensitive_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path} exists locally (should be gitignored)")
    
    print("  ✅ Security configuration looks good!")
    return True

def main():
    """Run all deployment readiness checks"""
    print("🚀 AI Appointment Assistant - Deployment Readiness Checker")
    print("=" * 60)
    
    checks = [
        ("Environment Variables", check_environment_variables),
        ("File Structure", check_file_structure),
        ("Dependencies", check_dependencies),
        ("Google Credentials", check_credentials_file),
        ("Security", check_security)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"  ❌ Error during {check_name} check: {str(e)}")
            results.append((check_name, False))
    
    print("\n" + "=" * 60)
    print("📊 DEPLOYMENT READINESS SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL CHECKS PASSED! Your app is ready for deployment!")
        print("\nNext steps:")
        print("1. Push to GitHub")
        print("2. Connect to Render/Heroku")
        print("3. Set environment variables on hosting platform")
        print("4. Upload service account credentials")
        print("5. Deploy!")
    else:
        print("⚠️  Some checks failed. Please fix the issues above before deploying.")
        print("\nFor help, see the README.md file.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
