#!/usr/bin/env python3
"""
Test script to verify the application works with existing dependencies
"""
import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if we can import all required modules"""
    try:
        import flask
        print(f"✓ Flask version: {flask.__version__}")
        
        import google.genai
        print("✓ Google GenAI imported successfully")
        
        import pydantic
        print(f"✓ Pydantic version: {pydantic.__version__}")
        
        from pydantic import BaseModel
        print("✓ Pydantic BaseModel imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_environment():
    """Test environment setup"""
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print(f"✓ GEMINI_API_KEY is set (length: {len(api_key)})")
    else:
        print("⚠ GEMINI_API_KEY not set - you'll need to set this before running the app")
    
    return True

if __name__ == "__main__":
    print("Testing AI Meal Plan Assistant dependencies...")
    print("=" * 50)
    
    if test_imports() and test_environment():
        print("\n✓ All tests passed! You can run the application.")
        print("\nTo run the app:")
        print("1. Set your GEMINI_API_KEY environment variable")
        print("2. Run: python app.py")
    else:
        print("\n✗ Some tests failed. Please check your installation.")
