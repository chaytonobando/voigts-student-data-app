#!/usr/bin/env python3
"""
🧪 Local Test Script for Voigts Student Data Processing Suite
Run this to test the app locally before deployment
"""

import sys
import os
import importlib

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing Python Imports...")
    
    required_modules = [
        ('streamlit', 'streamlit'),
        ('pandas', 'pandas'),
        ('base64', 'base64'),
        ('datetime', 'datetime'),
        ('io', 'io'),
        ('tempfile', 'tempfile'),
        ('pathlib', 'pathlib')
    ]
    
    optional_modules = [
        ('python-docx', 'docx'),
        ('reportlab', 'reportlab.pdfgen'),
        ('azure-ai-formrecognizer', 'azure.ai.formrecognizer'),
        ('pillow', 'PIL')
    ]
    
    print("\n📋 Required Modules:")
    all_required_ok = True
    for display_name, module_name in required_modules:
        try:
            importlib.import_module(module_name)
            print(f"  ✅ {display_name}")
        except ImportError as e:
            print(f"  ❌ {display_name}: {e}")
            all_required_ok = False
    
    print("\n📦 Optional Modules (for full functionality):")
    for display_name, module_name in optional_modules:
        try:
            importlib.import_module(module_name)
            print(f"  ✅ {display_name}")
        except ImportError:
            print(f"  ⚠️  {display_name}: Not installed (will use fallbacks)")
    
    return all_required_ok

def test_files():
    """Test that all required files exist"""
    print("\n📁 Testing File Structure...")
    
    required_files = [
        'streamlit_app.py',
        'requirements.txt',
        'README.md',
        'DEPLOYMENT_GUIDE.md',
        'Voigts Bus Service Logo.png'
    ]
    
    optional_files = [
        '.streamlit/secrets.toml',
        '.gitignore'
    ]
    
    print("\n📋 Required Files:")
    all_files_ok = True
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size:,} bytes)")
        else:
            print(f"  ❌ {file}: Missing!")
            all_files_ok = False
    
    print("\n📦 Optional Files:")
    for file in optional_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size:,} bytes)")
        else:
            print(f"  ⚠️  {file}: Missing (recommended)")
    
    return all_files_ok

def test_streamlit_syntax():
    """Test that the Streamlit app has valid Python syntax"""
    print("\n🐍 Testing Streamlit App Syntax...")
    
    try:
        with open('streamlit_app.py', 'r') as f:
            code = f.read()
        
        compile(code, 'streamlit_app.py', 'exec')
        print("  ✅ Python syntax is valid")
        return True
    except SyntaxError as e:
        print(f"  ❌ Syntax error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error reading file: {e}")
        return False

def main():
    """Run all tests"""
    print("🚌 Voigts Student Data Processing Suite - Local Testing")
    print("=" * 60)
    
    imports_ok = test_imports()
    files_ok = test_files()
    syntax_ok = test_streamlit_syntax()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"  Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"  Files:   {'✅ PASS' if files_ok else '❌ FAIL'}")
    print(f"  Syntax:  {'✅ PASS' if syntax_ok else '❌ FAIL'}")
    
    if imports_ok and files_ok and syntax_ok:
        print("\n🎉 All tests passed! Ready for deployment!")
        print("\n🚀 Next steps:")
        print("  1. Create GitHub repository")
        print("  2. Push code to GitHub")
        print("  3. Deploy on Streamlit Cloud")
        print("  4. Add Azure secrets")
        print("\n💡 Run: streamlit run streamlit_app.py (to test locally)")
    else:
        print("\n⚠️  Some tests failed. Please fix issues before deployment.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
